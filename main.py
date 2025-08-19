from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import shutil
from task_engine import process_task

app = FastAPI()   # 👈 must be at top level

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Home route
@app.get("/")
async def home():
    return {"message": "Welcome to TDS Project API. Use /healthz to check health or /api/ to upload files."}

# ✅ Health check route
@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

# ✅ File upload route
@app.post("/api/")
async def handle_files(files: list[UploadFile] = File(...)):
    saved_files = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file_path)

    try:
        result = process_task(saved_files)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

