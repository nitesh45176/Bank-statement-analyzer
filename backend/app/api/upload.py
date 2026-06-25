from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

router = APIRouter()


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):
    return {
        "filename": file.filename
    }