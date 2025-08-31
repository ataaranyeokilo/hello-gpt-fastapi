# hello-gpt-fastapi


## 📌 Project Goal
This project is a **lightweight LLM application** that demonstrates how to connect a FastAPI service to the **Azure OpenAI API**.  
The goal is to build a simple, production-ready foundation for more advanced GenAI systems such as **RAG chatbots, agentic AI workflows, and knowledge assistants**.

---

## 🎯 Objectives
- Set up a clean Python environment for AI engineering projects.
- Create a FastAPI service with a `/health` and `/ask` endpoint.
- Connect the service to Azure OpenAI (GPT model).
- Deploy the service locally and later to Azure App Service.
- Establish a foundation that will be extended in later weeks (RAG, GraphRAG, agents).

---

## 🛠️ Tech Stack
- **Python 3.9+**
- **FastAPI** — API framework
- **Uvicorn** — ASGI server
- **Azure OpenAI API** — LLM provider
- **python-dotenv** — environment variable management
- **requests** — for HTTP requests & testing

---

## ⚙️ How It Works
1. User sends a query to the `/ask` endpoint.  
2. FastAPI forwards the query to Azure OpenAI.  
3. Azure OpenAI processes the input and generates a response.  
4. FastAPI returns the answer as JSON to the user.  

---


# hello-got-fastapi
# hello-gpt-fastapi
