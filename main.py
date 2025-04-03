from fastapi import FastAPI, File, UploadFile
import shutil
import os
from moviepy.editor import VideoFileClip
from uuid import uuid4

app = FastAPI()

UPLOAD_FOLDER = "uploads"
GIF_FOLDER = "gifs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GIF_FOLDER, exist_ok=True)

@app.post("/convert")
async def convert_to_gif(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1]
    if file_extension.lower() not in ["mp4", "mov", "avi"]:
        return {"error": "Invalid file format. Please upload an MP4, MOV, or AVI file."}
    
    file_path = os.path.join(UPLOAD_FOLDER, f"{uuid4()}.{file_extension}")
    gif_path = os.path.join(GIF_FOLDER, f"{uuid4()}.gif")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        clip = VideoFileClip(file_path)
        clip = clip.set_duration(min(clip.duration, 10))  # Limit to 10 sec max
        clip.write_gif(gif_path, fps=10)
        
        os.remove(file_path)  # Remove original video to save space
        return {"message": "GIF created successfully!", "gif_url": gif_path}
    except Exception as e:
        return {"error": str(e)}
