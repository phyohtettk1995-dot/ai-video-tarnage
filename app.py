# -*- coding: utf-8 -*-
import os
import secrets
import shutil
import tempfile
from fastapi import FastAPI, Request, File, UploadFile, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import google.generativeai as genai

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

security = HTTPBasic()

# --- ဒီနေရာမှာ Username နဲ့ Password ကို ပြင်နိုင်ပါတယ် ---
USER_NAME = "admin"
USER_PASSWORD = "password123" 

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_ok = secrets.compare_digest(credentials.username, USER_NAME)
    is_pass_ok = secrets.compare_digest(credentials.password, USER_PASSWORD)
    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/")
async def index(request: Request, username: str = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/dub-video")
async def dub_video(
    file: UploadFile = File(...), 
    api_key: str = Form(...), 
    target_lang: str = Form(...)
):
    temp_file_path = ""
    try:
        genai.configure(api_key=api_key)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        video_file = genai.upload_file(path=temp_file_path)

        return {
            "status": "success", 
            "message": "အောင်မြင်ပါသည်။ ဗီဒီယိုကို Gemini သို့ တင်ပြီးပါပြီ။"
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
