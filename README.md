# ⚡ Zentro 2.0 – Intelligent Content Management  
### *Open-Source AI for Vision, Documents & RAG*  
### *Powered by Cyclops-VL 2.0 & Optimized for NVIDIA RTX GPUs*

![Zentro](https://img.shields.io/badge/Zentro-2.0-magenta?style=flat-square)
![Engine](https://img.shields.io/badge/Engine-Cyclops--VL%202.0%20%2B%20FastAPI-blue?style=flat-square)
![UI](https://img.shields.io/badge/UI-Streamlit%20(Custom%20CSS)-purple?style=flat-square)
![CUDA](https://img.shields.io/badge/Acceleration-RTX%20CUDA-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

> **Developed with ❤️ by Alan Cyril Sunny**  
> If you like this project, please ⭐ star the repository!

---

## 🧠 Zentro 2.0 – Offline Intelligent Content Platform

Zentro is an open-source intelligent content management platform designed for:

- **Image Analysis**  
- **Document Understanding**  
- **Retrieval-Augmented Conversational Intelligence (RAG)**  

It runs fully **offline**, powered by your **NVIDIA RTX GPU**, and uses **Cyclops-VL 2.0** for vision-language reasoning.

> ⚡ A commercial **cloud-managed version** also exists, where *all* computation, indexing, storage, and orchestration happen entirely in the cloud.

---

## ⚡ GPU Optimization (Open-Source Version)

- CUDA-accelerated model inference  
- Mixed-precision (AMP)  
- TensorRT-optimized model internals  
- GPU-accelerated embedding generation  
- Tuned for RTX GPUs (2050 → 4090 / A-Series)

---

## ✨ Features

### 🖼️ Zentro Vision – Image Intelligence
- Object, text & UI layout detection  
- Image captioning, reasoning & semantic understanding  
- Screenshot/diagram analysis  

### 📄 Zentro Docs – Document Intelligence
- High-accuracy PDF parsing using **PyMuPDF**  
- Layout + metadata extraction  
- Topic, summary, and entity understanding  

### 💬 Zentro Chat – RAG Conversational System
Complete offline RAG engine:

- **Persistent Knowledge Base** using ChromaDB  
- Multi-document chat & semantic retrieval  
- Context-aware memory with auto window management  
- Selective DB clearing and file-level control  

---

## 🧠 RAG Architecture

1. **Ingestion** → PDF/TXT via PyMuPDF  
2. **Chunking** → Optimized segmentation  
3. **Embedding** → SentenceTransformers (GPU)  
4. **Storage** → ChromaDB persistent vector store  
5. **Retrieval** → Semantic cosine similarity  
6. **LLM Answering** → Cyclops-VL 2.0 grounded generation  

---

## 🧩 Technology Stack

| Component | Technology |
|----------|------------|
| UI | Streamlit + Custom CSS |
| Backend | FastAPI |
| VLM | Cyclops-VL 2.0 |
| GPU Backend | CUDA (RTX) |
| Embeddings | SentenceTransformers |
| Vector Store | ChromaDB |
| Parsing | PyMuPDF (fitz) |
| API Model Interface | OpenAI-compatible (LM Studio) |
| Environment | Conda |

---

## 📁 Project Structure

```
zentro/
│── backend.py          # FastAPI backend server
│── streamlit_app.py    # Streamlit UI + Custom CSS
│── environment.yml     # Dependencies
│── README.md           # Documentation
│── run_backend.bat     # Backend launcher (Windows)
```

---

## 🌐 Commercial Cloud Version (Optional)

A premium **cloud-managed edition** of Zentro is also available.

In the cloud version:

- All computation  
- Document processing  
- Vector indexing  
- Retrieval + orchestration  
- Storage + management  

…are fully handled **in the cloud**.

### Additional cloud-only capabilities
- Multi-user workspaces  
- Automated ingestion pipelines  
- OCR + handwriting recognition  
- Knowledge graph generation  
- RBAC (Role-Based Access Control)  
- Dashboards, monitoring, auditing  

> 📌 This README documents the *offline open-source edition*.  
> The cloud version is a separate commercial product.

---

## 🔒 Privacy (Offline Version)

- 100% offline processing  
- Zero telemetry  
- No external APIs  
- All data stays on your device  

---

## 🚀 Running Zentro (Offline)

### 1. Start Backend

Using the batch script:
```bash
start run_backend.bat
```

Or manually:
```bash
uvicorn backend:app --reload --host 127.0.0.1 --port 8000
```

*(Ensure LM Studio is running and the model is loaded.)*

---

### 2. Start Frontend

```bash
streamlit run streamlit_app.py
```

---

### Access URLs

| Component | URL |
|----------|------|
| UI | http://localhost:8501 |
| Backend API | http://127.0.0.1:8000 |
| Health Check | http://127.0.0.1:8000/health |

---

## 🛠 Troubleshooting

### Backend not starting?
Check if port 8000 is in use:
```bash
netstat -ano | findstr :8000
```

### Context Length Errors
Zentro auto-manages context. If issues appear:

- Clear chat history  
- Reset knowledge base  

### GPU Not Detected?

```python
import torch
torch.cuda.is_available()
```

---

## 🤝 Contributing

Contributions are welcome!  
Fork the repo → Create a branch → Submit PR.

---

## 📜 License

MIT License — open, free, community-friendly.

---

## ⭐ Support the Project

If Zentro helps you, please ⭐ star the repository!

