from fastapi import FastAPI

from app.api.upload import router as upload_router


app = FastAPI(
    title="Bank Statement Analyzer"
)

app.include_router(upload_router)