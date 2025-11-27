# 🚀 Zentro 2.0 – Intelligent Content Management
### *Open-Source AI for Image, Document & Conversational Intelligence*
### *Powered by Cyclops-VL 2.0 & Optimized for NVIDIA RTX GPUs*

**Developed with ❤️ by Alan Cyril Sunny**

---

Zentro is an open-source intelligent content platform built for advanced image analysis, document understanding, and retrieval-augmented conversational intelligence (RAG).
It operates fully offline on your machine and is optimized for NVIDIA RTX GPUs.

> ⚡ A commercial **cloud-managed version** also exists, where all computation, processing, indexing, storage, and orchestration run entirely in the cloud.

---

## ⚡ GPU Optimization (Open-Source Version)

- CUDA-accelerated inference
- Mixed Precision (AMP)
- TensorRT-friendly model architecture
- GPU-accelerated embedding generation
- Optimized for RTX 2050 → 4090 & A-series  

---

## ✨ Key Features

### 🖼️ Zentro Vision – Image Intelligence
- Object, text, and layout detection
- Diagram & UI screenshot analysis
- Image summarization & reasoning

### 📄 Zentro Docs – Document Intelligence
- **Better PDF Parsing**: Powered by `PyMuPDF` for accurate text extraction.
- Metadata extraction
- Structured summaries, entities & topics

### 💬 Zentro Chat – RAG-Powered Conversational AI
Includes a complete offline Retrieval-Augmented Generation system:

- **Persistent Knowledge Base**: Documents are indexed in `ChromaDB` and persist across restarts.
- **Multi-Document RAG**: Chat with multiple documents simultaneously.
- **Context-Aware Chat**: Remembers conversation history for natural follow-ups.
- **Smart Context Management**: Automatically handles long documents and histories to fit model context windows.
- **Knowledge Base Management**: Clear the database or select specific files to chat with.

### 🎨 Premium UI Experience
- **Modern Dark Theme**: Glassmorphism design with custom CSS.
- **Interactive Elements**: Animated buttons and styled chat bubbles.
- **Settings Sidebar**: Configure backend URLs and manage your knowledge base easily.

---

## 🧠 Zentro RAG Architecture

1. **Ingestion** → PDF/TXT loading via `PyMuPDF`
2. **Chunking** → Optimized text segmentation
3. **Embedding** → `SentenceTransformers` (GPU accelerated)
4. **Storage** → `ChromaDB` Persistent Vector Store
5. **Retrieval** → Semantic search (Cosine Similarity)
6. **Answering** → Cyclops-VL 2.0 generates grounded responses

---

## 🧩 Technology Stack

| Component | Technology |
|----------|------------|
| UI | Streamlit (Custom CSS) |
| Backend | FastAPI |
| Vision-Language Model | Cyclops-VL 2.0 |
| GPU Acceleration | CUDA + RTX |
| Embeddings | SentenceTransformers |
| Vector Store | ChromaDB |
| Parsing | PyMuPDF (fitz) |
| API Format | OpenAI-compatible (LM Studio) |
| Environment | Conda |

---

## 📦 Project Structure

```
zentro/
│── backend.py          # FastAPI Backend
│── streamlit_app.py    # Streamlit Frontend
│── environment.yml     # Dependencies
│── README.md           # Documentation
│── run_backend.bat     # Startup Script
```

---

## 🌐 Commercial Cloud Version (Optional)

Alongside the offline open-source version, Zentro is also available as a **fully cloud-managed commercial offering**.

In the cloud version:

- All computation
- All data processing
- All document analysis
- All retrieval, indexing, and similarity search
- All orchestration and automation
- All storage and management  

…are handled entirely **in the cloud**, requiring no local hardware.

Extra cloud capabilities include:

- Multi-user workspace
- Document ingestion pipelines
- OCR + handwriting recognition
- Knowledge graph generation
- Centralized storage
- Role-based access control
- Audit logs and monitoring dashboards  

> 📌 This README describes the offline open-source version.  
> The cloud-managed version is a separate commercial product.

---

## 🔒 Privacy (Open-Source Version)

- Fully offline  
- No telemetry
- No external APIs  
- All data stays on-device

---

## 🚀 Running Zentro (Offline Version)

### 1. Start Backend
Use the provided batch script or run manually:
```bash
start run_backend.bat
# OR
uvicorn backend:app --reload --host 127.0.0.1 --port 8000
```
*Note: Ensure LM Studio is running and the model is loaded.*

### 2. Start Frontend
```bash
streamlit run streamlit_app.py
```

### Access Points
- **UI**: `http://localhost:8501`
- **Backend API**: `http://127.0.0.1:8000`
- **Health Check**: `http://127.0.0.1:8000/health`

---

## 🛠 Troubleshooting

### Backend not running
Check if port 8000 is free.
```bash
netstat -ano | findstr :8000
```

### Context Overflow Errors
Zentro automatically manages context, but if you see errors, try clearing the chat history or knowledge base.

### GPU not detected
```python
import torch
torch.cuda.is_available()
```

---

## 🤝 Contributing

Contributions are welcome!

---

## 📜 License  
MIT License

---

## ⭐ Support  
If Zentro helps you, star ⭐ the repo!
