import os
from fastapi import HTTPException
from fastapi.responses import FileResponse

BASE_PATH = "/app/files"   # ← mapped to NFS

def get_full_path(relative_path: str):
    return os.path.join(BASE_PATH, relative_path)

def serve_file(relative_path: str, user):
    file_path = get_full_path(relative_path)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # 🔐 TODO: implement proper access check
    if not has_access(user, relative_path):
        raise HTTPException(status_code=403, detail="Access denied")

    return FileResponse(file_path)


def has_access(user, relative_path):
    # TEMP basic logic (improve later)
    if user.role == "admin":
        return True

    if str(user.id) in relative_path:
        return True

    return False