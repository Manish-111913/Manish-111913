# AI Industrial Knowledge Intelligence Platform

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-Graph_DB-008CC1?logo=neo4j&logoColor=white)](https://neo4j.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Orchestration-1C3C3A)](https://www.langchain.com/)
[![React](https://img.shields.io/badge/React-Frontend-20232A?logo=react&logoColor=61DAFB)](https://react.dev/)

An enterprise-grade industrial AI platform that integrates **Retrieval-Augmented Generation (RAG)** with a **Knowledge Graph** database (GraphRAG). This system transforms complex industrial manuals, documentation, and operational data into structured, queried knowledge, enabling intelligent cross-document analysis, semantic search, and hallucination-free AI reasoning.

---

## 🔗 Architecture Overview

```
                      +-------------------+
                      |  Industrial PDFs  |
                      +---------+---------+
                                |
                                v
                   +------------+------------+
                   |  Entity Extraction &    |
                   |   Knowledge Graph Gen   |
                   +------------+------------+
                                |
                                v
                      +---------+---------+
                      |   Neo4j Graph DB  | <------+
                      +---------+---------+        |
                                |                  | Hybrid Search
                                v                  | (Graph + Vector)
                      +---------+---------+        |
                      | Vector Embeddings | <------+
                      +---------+---------+
                                |
                                v
     +--------+       +---------+---------+       +--------+
     |  User  | ----> |  FastAPI Backend  | ----> | LLM    |
     | React  | <---- | (LangChain RAG)   | <---- | Gemini |
     +--------+       +-------------------+       +--------+
```

---

## ⚡ Features

- **Hybrid Graph-Vector Search (GraphRAG)**: Integrates vector similarity search with structured graph database traversals to retrieve highly context-rich answers.
- **Entity & Relation Extraction**: Automatically extracts industrial entities (Equipment, Sensors, Procedures, Faults) and maps their dependencies.
- **Dynamic Knowledge Graph Visualization**: Interactive graph interface in the frontend allowing users to traverse nodes and edges visually.
- **Explainable AI**: The system outputs the graph paths traversed to reach the generated answer, ensuring auditable responses for industrial safety.
- **Multimodal Data Support**: Processes scanned schematics, technical tables, and PDFs.

---

## 💻 Tech Stack

- **Frontend**: React, Tailwind CSS, Cytoscape.js (for graph rendering)
- **Backend API**: FastAPI, Python
- **Orchestration**: LangChain & LlamaIndex
- **Databases**: Neo4j (Graph DB), Qdrant / pgvector (Vector DB)
- **AI Models**: Gemini 1.5 Pro / GPT-4o (Reasoning & Graph generation), text-embedding-004 (Embeddings)

---

## 🛠️ Installation & Setup

### Prerequisites
- Neo4j Database instance running (local or AuraDB cloud)
- Python 3.10+
- Node.js 18+

### Step 1: Clone the Repository
```bash
git clone https://github.com/Manish-111913/AI-Knowledge-Platform.git
cd AI-Knowledge-Platform
```

### Step 2: Configure Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a `.env` file based on `.env.example`:
   ```env
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_secure_password
   GEMINI_API_KEY=your_gemini_api_key
   QDRANT_HOST=localhost
   QDRANT_PORT=6333
   ```
3. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/Scripts/activate # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Start the backend:
   ```bash
   uvicorn main:app --reload
   ```

### Step 3: Configure Frontend
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies and start the app:
   ```bash
   npm install
   npm run dev
   ```

---

## 📂 Folder Structure

```
AI-Knowledge-Platform/
├── backend/
│   ├── app/
│   │   ├── core/           # RAG search logic & database connections
│   │   ├── pipelines/      # PDF processing & Graph generation pipelines
│   │   └── api/            # FastAPI endpoints
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/     # Visual Graph rendering & chat screens
│   │   └── App.jsx
│   ├── package.json
│   └── tailwind.config.js
├── README.md
└── architecture.png
```

---

## 🚀 Future Scope

- Integration with real-time SCADA sensor streams to overlay live telemetry onto graph nodes.
- Local deployment of specialized open-source LLMs (e.g., Llama-3-70B) for offline air-gapped security in enterprise factories.

---

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.
