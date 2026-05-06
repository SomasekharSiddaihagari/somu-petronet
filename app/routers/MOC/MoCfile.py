from fastapi import APIRouter, UploadFile, File as FastAPIFile, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
import shutil

from app.database import get_db
from app.routers.UserAuthR2 import make_download_url
from app.schemas.MOC.MoCFile import FileOut
from app.models.MOC.MocfileModel import File
from app.crud.MOC import MoCFile

router = APIRouter(prefix="/moc/files", tags=["MOC Files"])

UPLOAD_ROOT = "C:/Petronet/files/moc_files"
os.makedirs(UPLOAD_ROOT, exist_ok=True)

@router.post("/upload", response_model=List[FileOut])
async def upload_moc_files(
    moc_request_id: int,
    moc_request_no: str,
    files: List[UploadFile] = FastAPIFile(...),
    db: Session = Depends(get_db),
):
    """Upload multiple files for a specific MOC request"""
    
    # Directory for this MOC request
    moc_dir = os.path.join(UPLOAD_ROOT, )
    os.makedirs(moc_dir, exist_ok=True)

    uploaded_files = []

    for file in files:
        # file_path = os.path.join(moc_dir, file.filename)
        file_path=f"{moc_dir}/{file.filename}"
        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ✅ Save record to database properly
        db_file = File(
            filename=file.filename,
            filepath=file_path,
            model_id=moc_request_id,
            model_name=moc_request_no,
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        uploaded_files.append(db_file)

    return uploaded_files


@router.get("/by-id/{moc_id}", response_model=List[FileOut])
def get_files_by_moc_id(moc_id: int, db: Session = Depends(get_db)):
    """Fetch all files by MOC ID with downloadable links"""

    files = MoCFile.get_files_by_model_id(db, moc_id)

    if not files:
        raise HTTPException(status_code=404, detail="No files found for this MOC ID")

    response = []

    for file in files:
        file.download_url = make_download_url(file.filepath)
        response.append(file)

    return response



# @router.get("/by-name/{moc_name}", response_model=List[FileOut])
# def get_files_by_moc_name(moc_name: str, db: Session = Depends(get_db)):
#     """Fetch all files by MOC name"""
#     files = MoCFile.get_files_by_model_name(db, moc_name)
#     if not files:
#         raise HTTPException(status_code=404, detail="No files found for this MOC name")
#     return files
from fastapi.responses import FileResponse

@router.get("/download/{file_id}")
def download_moc_file(file_id: int, db: Session = Depends(get_db)):
    """Download a specific MOC file by ID"""
    db_file = MoCFile.get_file_by_id(db, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found in database")

    if not os.path.exists(db_file.filepath):
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        path=db_file.filepath,
        filename=db_file.filename,
        media_type="application/octet-stream"
    )
@router.put("/upload", response_model=List[FileOut])
async def update_moc_files(
    moc_request_id: int,
    moc_request_no: str,
    files: List[UploadFile] = FastAPIFile(...),
    db: Session = Depends(get_db),
):
    """Replace uploaded files for a specific MOC request"""

    # Directory for this MOC request
    moc_dir = os.path.join(UPLOAD_ROOT, str(moc_request_id))
    os.makedirs(moc_dir, exist_ok=True)

    # 🔥 Delete existing file records
    existing_files = (
        db.query(File)
        .filter(
            File.model_id == moc_request_id,
            File.model_name == moc_request_no,
        )
        .all()
    )

    for ef in existing_files:
        # Optional: delete physical file
        if ef.filepath and os.path.exists(ef.filepath):
            os.remove(ef.filepath)

        db.delete(ef)

    db.commit()

    uploaded_files = []

    for file in files:
        file_path = os.path.join(moc_dir, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        db_file = File(
            filename=file.filename,
            filepath=file_path,
            model_id=moc_request_id,
            model_name=moc_request_no,
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        uploaded_files.append(db_file)

    return uploaded_files
@router.delete("/{file_id}")
def delete_moc_file(file_id: int, db: Session = Depends(get_db)):
    """Delete MOC file entry from database only"""

    db_file = db.query(File).filter(File.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    db.delete(db_file)
    db.commit()

    return {
        "detail": f"File record '{db_file.filename}' deleted successfully"
    }
