from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import joblib
import pandas as pd
import random
import os

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="static")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only. Restrict in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
resources_path = "quotes.pkl"
if not os.path.exists(resources_path):
    raise FileNotFoundError(f"{resources_path} file not found.")

def load_resources():
    resources = joblib.load(resources_path)
    return resources["data"]

data = load_resources()

# Input models
class InputPhrase(BaseModel):
    phrase: str

class AnswersModel(BaseModel):
    title: str
    author: str
    user_answers: list

def get_random_quote(input_phrase: str):
    if not input_phrase.strip():
        raise ValueError("Input phrase cannot be empty.")
    matching_quotes = data[data['Kelimeler'].str.contains(input_phrase, case=False, na=False)]
    if not matching_quotes.empty:
        random_index = random.choice(matching_quotes.index)
        selected_quote = matching_quotes.loc[random_index]
        return {
            "Title": selected_quote['Title'],
            "Author": selected_quote['Author'],
            "Text": selected_quote['Text']
        }
    else:
        return None

def display_questions():
    return [
        "1. Bu metin size ne ifade ediyor?",
        "2. Metindeki ana mesajı nasıl yorumlarsınız?",
        "3. Bu metnin günlük hayatınıza bir katkısı olabilir mi? Eğer evet, nasıl?"
    ]

@app.post("/get_quote")
def get_quote(input_phrase: InputPhrase):
    try:
        result = get_random_quote(input_phrase.phrase)
        if result:
            response = {
                "title": result["Title"],
                "author": result["Author"],
                "text": result["Text"],
                "questions": display_questions()
            }
            return response
        else:
            raise HTTPException(status_code=404, detail="No matching quote found.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/submit_answers")
def submit_answers(answers: AnswersModel):
    # In a real scenario, you might save this to a database.
    print("Received Answers:")
    print("Title:", answers.title)
    print("Author:", answers.author)
    for idx, ans in enumerate(answers.user_answers, start=1):
        print(f"Answer {idx}: {ans}")
    return {"status": "success", "message": "Answers received successfully."}

@app.get("/", response_class=HTMLResponse)
def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/online", response_class=JSONResponse)
def online(request: Request):
    return {"status": "online"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)