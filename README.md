###############################################################
#                                                             #
#     ███████╗███████╗███╗   ███╗████████╗██████╗  ██████╗    #
#     ██╔════╝██╔════╝████╗ ████║╚══██╔══╝██╔══██╗██╔════╝    #
#     ███████╗█████╗  ██╔████╔██║   ██║   ██████╔╝██║         #
#     ╚════██║██╔══╝  ██║╚██╔╝██║   ██║   ██╔══██╗██║         #
#     ███████║███████╗██║ ╚═╝ ██║   ██║   ██║  ██║╚██████╗    #
#     ╚══════╝╚══════╝╚═╝     ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝    #
#                                                             #
#               ZENTRO 2.0 — INTELLIGENT CONTENT              #
#                   Offline Vision • Docs • RAG               #
###############################################################

```

```
               ______
            .-'      `-.
          .'            `.
         /   ZENTRO 2.0   \
        |   (AI Platform)  |
        |      _____       |
         \    (  Z  )     /
          `.    ----    .'
            `-.______.-'
```

# ⚡ Zentro 2.0 – Intelligent Content Management  
### *Open-Source AI for Vision, Documents & RAG (Offline, GPU-Optimized)*  
### *Built by Alan Cyril Sunny*

---

## 🔰 ASCII Tech Badges (GitHub-safe)

```
[ Engine: Cyclops-VL 2.0 ] [ UI: Streamlit ] [ Backend: FastAPI ]
[ GPU: CUDA RTX ] [ Embeddings: SentenceTransformers ] [ DB: ChromaDB ]
[ Parsing: PyMuPDF ] [ License: MIT ] [ Mode: Fully Offline ]
```

---

# 📚 Table of Contents

- [🚀 Overview](#-overview)
- [⚡ GPU Optimization](#-gpu-optimization)
- [✨ Features](#-features)
- [🧠 RAG Architecture](#-rag-architecture)
- [🧩 Technology Stack](#-technology-stack)
- [📁 Project Structure](#-project-structure)
- [🌐 Cloud Edition](#-cloud-edition)
- [🔒 Privacy](#-privacy)
- [🚀 Running Zentro](#-running-zentro)
- [🛠 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [⭐ Support](#-support)

---

# 🚀 Overview

Zentro 2.0 is an **offline, open-source AI platform** for:

- 🖼️ Image Intelligence  
- 📄 Document Intelligence  
- 💬 RAG-powered conversational AI  

Runs **100% locally** with **RTX GPU acceleration**.

> A commercial **cloud-managed edition** also exists  
> where all compute, processing, indexing, storage, and orchestration  
> run entirely in the cloud.

---

# ⚡ GPU Optimization

- CUDA-accelerated inference  
- Mixed precision (AMP)  
- TensorRT-compatible architecture  
- GPU-accelerated embeddings  
- Optimized for:  
  `RTX 2050 → 4060 → 4090 → A-Series`

---

# ✨ Features

## 🖼️ Zentro Vision — Image Intelligence
- Object/text/layout detection  
- Diagram & UI screenshot understanding  
- Image reasoning, summaries, captions  

## 📄 Zentro Docs — Document Intelligence
- High-accuracy parsing using **PyMuPDF**  
- Layout + metadata extraction  
- Topic modeling, entity extraction, structured summaries  

## 💬 Zentro Chat — RAG Conversational AI
- Persistent knowledge base via **ChromaDB**  
- Multi-document RAG  
- Context-aware follow-ups  
- Auto context window management  
- Clear/reset knowledge base on demand  

---

# 🧠 RAG Architecture

```
[ Ingestion ] → [ Chunking ] → [ Embedding ] → [ ChromaDB ]
       ↓               ↓              ↓               ↓
                [ Semantic Retrieval ] → [ LLM Answering ]
```

- **Ingestion**: PyMuPDF PDF/TXT loader  
- **Chunking**: smart segmentation  
- **Embedding**: SentenceTransformers (GPU)  
- **Retrieval**: cosine similarity  
- **LLM**: Cyclops-VL 2.0  

---

# 🧩 Technology Stack

```
UI             → Streamlit + Custom CSS  
Backend        → FastAPI  
AI Model       → Cyclops-VL 2.0  
GPU Engine     → CUDA (RTX)  
Embeddings     → SentenceTransformers  
Vector Store   → ChromaDB  
Parsing        → PyMuPDF (fitz)  
API Format     → OpenAI Compatible (LM Studio)  
Environment    → Conda  
```

---

# 📁 Project Structure

```
zentro/
│── backend.py          # FastAPI backend
│── streamlit_app.py    # Streamlit UI
│── environment.yml     # Dependencies
│── README.md           # Documentation
│── run_backend.bat     # Backend launcher
```

---

# 🌐 Cloud Edition

A fully cloud-managed version is available (commercial).

Cloud version provides:

- Multi-user workspaces  
- OCR + handwriting recognition  
- Automated ingestion pipelines  
- Knowledge graph generation  
- Centralized vector database  
- RBAC (roles & permissions)  
- Monitoring dashboards  

This README focuses on the **offline open-source version**.

---

# 🔒 Privacy

- Fully offline  
- No external APIs  
- No telemetry  
- All data stays on your device  

---

# 🚀 Running Zentro

## 1️⃣ Start Backend
```
start run_backend.bat
```
or
```
uvicorn backend:app --reload --host 127.0.0.1 --port 8000
```

## 2️⃣ Start Frontend
```
streamlit run streamlit_app.py
```

## Access
```
UI        → http://localhost:8501
Backend   → http://127.0.0.1:8000
Health    → http://127.0.0.1:8000/health
```

---

# 🛠 Troubleshooting

### Backend port busy
```
netstat -ano | findstr :8000
```

### Context overflow
- Clear history  
- Reset knowledge base  

### GPU not detected
```
import torch
torch.cuda.is_available()
```

---

# 🤝 Contributing

Pull requests welcome!  
Fork → Branch → PR.

---

# 📜 License

MIT License.

---

# ⭐ Support

If Zentro helps you,  
**please ⭐ star the repository!**

