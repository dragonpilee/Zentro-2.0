print("Starting script...", flush=True)
import base64
import io
import os
import uuid
from typing import Dict, List, Optional

import numpy as np
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
import chromadb
import fitz  # PyMuPDF
# from sentence_transformers import SentenceTransformer

print("Imports done.", flush=True)

# =========================
# CONFIG
# =========================

# LM Studio server (OpenAI-compatible)
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://127.0.0.1:1234/v1")
LM_STUDIO_API_KEY = os.getenv("LM_STUDIO_API_KEY", "lm-studio")  # dummy key, LM Studio ignores it

# Model names as shown in LM Studio
QWEN_VL_MODEL_NAME = os.getenv("QWEN_VL_MODEL_NAME", "qwen/qwen3-vl-4b-instruct")
QWEN_CHAT_MODEL_NAME = os.getenv("QWEN_CHAT_MODEL_NAME", QWEN_VL_MODEL_NAME)

client = OpenAI(
    base_url=LM_STUDIO_BASE_URL,
    api_key=LM_STUDIO_API_KEY,
)

# Global variable for lazy loading
_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        print("Lazy loading SentenceTransformer...", flush=True)
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        print("Lazy loaded.", flush=True)
    return _embedding_model

# Persistent Vector Store
print("Initializing ChromaDB...", flush=True)
CHROMA_CLIENT = chromadb.PersistentClient(path="./chroma_db")
COLLECTION = CHROMA_CLIENT.get_or_create_collection(name="zentro_docs")
print("ChromaDB initialized.", flush=True)

app = FastAPI(title="Qwen Backend")

# Allow Streamlit on localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# HELPERS
# =========================

def encode_image_to_data_url(file_bytes: bytes, mime_type: str) -> str:
    b64 = base64.b64encode(file_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{b64}"


def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def guess_mime_type(file_name: str) -> str:
    f = file_name.lower()
    if f.endswith(".png"):
        return "image/png"
    if f.endswith(".jpg") or f.endswith(".jpeg"):
        return "image/jpeg"
    if f.endswith(".webp"):
        return "image/webp"
    return "application/octet-stream"


def chunk_text(text: str, max_chars: int = 800) -> List[str]:
    """Simple chunker by characters with paragraph splitting."""
    paragraphs = text.split("\n\n")
    chunks: List[str] = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= max_chars:
            current += ("\n\n" + para) if current else para
        else:
            if current:
                chunks.append(current)
            current = para

    if current:
        chunks.append(current)

    return chunks


def call_qwen_chat(messages, model_name: Optional[str] = None, temperature: float = 0.2) -> str:
    model_name = model_name or QWEN_CHAT_MODEL_NAME
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/analyze/image")
async def analyze_image(
    file: UploadFile = File(...),
    instruction: str = Form("Describe this image in detail."),
):
    file_bytes = await file.read()
    mime_type = guess_mime_type(file.filename)

    data_url = encode_image_to_data_url(file_bytes, mime_type)

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": instruction},
                {"type": "image_url", "image_url": {"url": data_url}},
            ],
        }
    ]

    try:
        result = call_qwen_chat(messages, model_name=QWEN_VL_MODEL_NAME)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


@app.post("/analyze/document")
async def analyze_document(
    file: UploadFile = File(...),
    instruction: str = Form("Summarize this document and extract key points, entities, and dates."),
):
    file_bytes = await file.read()
    name = file.filename.lower()

    if name.endswith(".txt"):
        try:
            text = file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            text = file_bytes.decode("latin-1", errors="ignore")
    elif name.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    else:
        return {"error": "Unsupported file type. Use PDF or TXT."}

    if not text.strip():
        return {"error": "No text extracted from document."}

    truncated = text[:4000]

    prompt = (
        f"You are an AI assistant analyzing a document.\n\n"
        f"USER INSTRUCTION:\n{instruction}\n\n"
        f"DOCUMENT CONTENT (possibly truncated):\n{truncated}"
    )

    messages = [{"role": "user", "content": prompt}]

    try:
        result = call_qwen_chat(messages)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


@app.post("/rag/upload")
async def rag_upload(
    file: UploadFile = File(...),
):
    try:
        file_bytes = await file.read()
        name = file.filename.lower()

        if name.endswith(".txt"):
            try:
                text = file_bytes.decode("utf-8", errors="ignore")
            except Exception:
                text = file_bytes.decode("latin-1", errors="ignore")
        elif name.endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
        else:
            return {"error": "Unsupported file type. Use PDF or TXT."}

        if not text.strip():
            return {"error": "No text extracted from document."}

        chunks = chunk_text(text, max_chars=800)
        
        # Generate IDs and Metadata
        doc_id = str(uuid.uuid4())
        ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
        metadatas = [{"doc_id": doc_id, "filename": file.filename, "chunk_index": i} for i in range(len(chunks))]

        # Add to ChromaDB (it handles embeddings if we don't provide them, but we have a model)
        # We will use our own embeddings to be consistent
        model = get_embedding_model()
        embeddings = model.encode(chunks).tolist()
        
        COLLECTION.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )

        preview = text[:1000]

        return {
            "doc_id": doc_id,
            "num_chunks": len(chunks),
            "file_name": file.filename,
            "preview": preview,
        }
    except Exception as e:
        print(f"Error in rag_upload: {e}", flush=True)
        return {"error": str(e)}


@app.get("/rag/list")
async def rag_list():
    try:
        # Get all metadata to find unique documents
        # In a real app, you'd have a separate SQL db for metadata, but this works for now
        data = COLLECTION.get(include=["metadatas"])
        docs = {}
        if data["metadatas"]:
            for meta in data["metadatas"]:
                if meta:
                    docs[meta["doc_id"]] = meta["filename"]
        return {"documents": [{"doc_id": k, "filename": v} for k, v in docs.items()]}
    except Exception as e:
        return {"error": str(e)}


@app.post("/rag/clear")
async def rag_clear():
    try:
        # Delete and recreate the collection
        CHROMA_CLIENT.delete_collection("zentro_docs")
        global COLLECTION
        COLLECTION = CHROMA_CLIENT.get_or_create_collection(name="zentro_docs")
        return {"status": "success", "message": "Knowledge base cleared."}
    except Exception as e:
        return {"error": str(e)}


class RAGQuestion(BaseModel):
    doc_id: Optional[str] = None
    question: str
    instruction: Optional[str] = None
    chat_history: List[Dict[str, str]] = []


@app.post("/rag/ask")
async def rag_ask(body: RAGQuestion):
    try:
        # Search in ChromaDB
        # If doc_id is provided, filter by it. Otherwise search all.
        where_filter = {"doc_id": body.doc_id} if body.doc_id else None
        
        model = get_embedding_model()
        q_vec = model.encode([body.question]).tolist()
        
        results = COLLECTION.query(
            query_embeddings=q_vec,
            n_results=2,
            where=where_filter
        )
        
        if not results["documents"] or not results["documents"][0]:
            return {"answer": "I couldn't find any relevant information in the documents."}

        retrieved_chunks = results["documents"][0]
        
        context_text = "\n\n".join(retrieved_chunks)

        instruction = body.instruction or (
            "Using only the context chunks below, answer the user's question. "
            "If the answer is not clearly in the context, say you don't know."
        )
        
        # Construct History
        # Convert chat_history to the format expected by the LLM (if needed)
        # Here we just append the new prompt
        
        messages = []
        if body.chat_history:
            # Limit history to last 4 messages and truncate content
            for msg in body.chat_history[-4:]:
                content = msg.get("content", "")
                if len(content) > 500:
                    content = content[:500] + "..."
                messages.append({"role": msg["role"], "content": content})

        prompt = (
            f"{instruction}\n\n"
            f"CONTEXT CHUNKS:\n{context_text}\n\n"
            f"USER QUESTION:\n{body.question}"
        )
        
        # Hard limit on prompt length (approx 3500 chars ~ 1000 tokens)
        if len(prompt) > 3500:
            prompt = prompt[:3500] + "... [TRUNCATED]"
        
        messages.append({"role": "user", "content": prompt})

        answer = call_qwen_chat(messages)
        return {
            "answer": answer,
            "used_chunks": results["ids"][0],
        }
    except Exception as e:
        print(f"Error in rag_ask: {e}", flush=True)
        return {"error": str(e)}


if __name__ == "__main__":
    print("Starting backend...", flush=True)
    import uvicorn
    print("Imported uvicorn", flush=True)
    host = os.getenv("HOST", "127.0.0.1")
    uvicorn.run(app, host=host, port=8000)
