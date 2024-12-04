from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import os

app = FastAPI()

# Static dosyaları sunmak için
static_path = "static"
if not os.path.exists(static_path):
    raise FileNotFoundError(f"{static_path} klasörü bulunamadı.")
app.mount("/static", StaticFiles(directory=static_path), name="static")

# CORS middleware ekleyelim
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model ve verileri yükleme
resources_path = "quotes.pkl"
if not os.path.exists(resources_path):
    raise FileNotFoundError(f"{resources_path} dosyası bulunamadı.")

def load_resources():
    resources = joblib.load(resources_path)
    return resources["model"], resources["vectorizer"], resources["data"]

model, vectorizer, data = load_resources()

# Giriş modeli
class InputPhrase(BaseModel):
    phrase: str

# Endpoint: Alıntı döndürme
@app.post("/get_quote")
def get_quote(input_phrase: InputPhrase):
    if not input_phrase.phrase.strip():
        raise HTTPException(status_code=400, detail="Lütfen geçerli bir metin girin.")

    input_vector = vectorizer.transform([input_phrase.phrase])
    distances, indices = model.kneighbors(input_vector, n_neighbors=5)

    # Rasgele bir alıntı seçme
    closest_index = np.random.choice(np.array(indices[0]))
    closest_quote = data.iloc[closest_index]

    response = {
        "title": closest_quote["Title"],
        "author": closest_quote["Author"],
        "text": closest_quote["Text"],
        "questions": [
            "Bu metin size ne ifade ediyor?",
            "Metindeki ana mesajı nasıl yorumlarsınız?",
            "Bu metnin günlük hayatınıza bir katkısı olabilir mi? Eğer evet, nasıl?"
        ]
    }
    return response

# Ana endpoint (index.html'i döndürme)
@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = os.path.join(static_path, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html dosyası bulunamadı.")
    with open(index_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)
