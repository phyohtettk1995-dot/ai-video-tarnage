# -*- coding: utf-8 -*-
import os
import secrets
import shutil
import asyncio
from edge_tts import Communicate
from moviepy.editor import VideoFileClip, AudioFileClip
from fastapi import FastAPI, Request, File, UploadFile, Form, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import google.generativeai as genai

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DOWNLOADS_DIR = "downloads"
for folder in [DOWNLOADS_DIR, "static"]:
    if not os.path.exists(folder): os.makedirs(folder)

app.mount("/static", StaticFiles(directory="static"), name="static")
security = HTTPBasic()

USER_NAME = "admin"
USER_PASSWORD = "password123"

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if not (secrets.compare_digest(credentials.username, USER_NAME) and 
            secrets.compare_digest(credentials.password, USER_PASSWORD)):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.username

@app.get("/")
async def index(request: Request, username: str = Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/dub-video")
async def dub_video(file: UploadFile = File(...), api_key: str = Form(...)):
    unique_id = secrets.token_hex(4)
    input_video = os.path.join(DOWNLOADS_DIR, f"in_{unique_id}.mp4")
    temp_audio = os.path.join(DOWNLOADS_DIR, f"v_{unique_id}.mp3")
    output_video = os.path.join(DOWNLOADS_DIR, f"out_{unique_id}.mp4")

    try:
        with open(input_video, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        video_part = genai.upload_file(path=input_video)
        
        prompt = "Translate all speech in this video to natural Myanmar (Burmese). Return only the translated text."
        response = model.generate_content([prompt, video_part])
        myanmar_text = response.text

        # မြန်မာအသံဖန်တီးခြင်း
        communicate = Communicate(text=myanmar_text, voice="my-MM-ThihaNeural")
        await communicate.save(temp_audio)

        # Video နဲ့ Audio ပေါင်းခြင်း
        video_clip = VideoFileClip(input_video)
        myanmar_audio = AudioFileClip(temp_audio)
        
        final_clip = video_clip.set_audio(myanmar_audio)
        final_clip.write_videofile(output_video, codec="libx264", audio_codec="aac", temp_audiofile=os.path.join(DOWNLOADS_DIR, f"temp_{unique_id}.m4a"), remove_temp=True)

        video_clip.close()
        myanmar_audio.close()

        return {
            "status": "success",
            "message": "Dubbing အောင်မြင်ပါသည်။",
            "mp3_url": f"/download/{os.path.basename(temp_audio)}",
            "mp4_url": f"/download/{os.path.basename(output_video)}"
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(DOWNLOADS_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path)
    raise HTTPException(status_code=404, detail="File not found")
