from fastapi import FastAPI
from app.api.upload import router as upload_router


app = FastAPI(
    title="Multimodal RAG",
    version="0.1.0",
)


app.include_router(upload_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }