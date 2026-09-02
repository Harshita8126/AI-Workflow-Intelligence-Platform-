from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import attrition, dashboard, skills, rag, agent
from app.utils.logger import app_logger
from app.ml.model_loader import ModelRegistry

@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info("Starting Enterprise HR AI FastAPI Backend on localhost:8000...")
    ModelRegistry.get_instance()
    app_logger.info("Model and Services initialized successfully.")
    yield
    app_logger.info("Shutting down Enterprise HR AI Backend...")

app = FastAPI(
    title="Enterprise HR AI — Workforce Intelligence & Upskilling Platform",
    description="Locally runnable enterprise HR intelligence API predicting attrition, computing skill gaps, ranking learning recommendations, answering policy queries via RAG, and orchestrating governed workforce agents.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(attrition.router)
app.include_router(dashboard.router)
app.include_router(skills.router)
app.include_router(rag.router)
app.include_router(agent.router)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Enterprise HR AI Platform API",
        "version": "1.0.0",
        "docs_url": "/docs"
    }
