from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import random
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

# Model ve veri yükleme
resources_path = "quotes.pkl"
if not os.path.exists(resources_path):
    raise FileNotFoundError(f"{resources_path} dosyası bulunamadı.")

def load_resources():
    resources = joblib.load(resources_path)
    return resources["data"]

# Veriyi yükleyelim
data = load_resources()

# Giriş modeli
class InputPhrase(BaseModel):
    phrase: str

# Alıntı seçme fonksiyonu
def get_random_quote(input_phrase: str):
    if not input_phrase.strip():
        raise ValueError("Girdi boş olamaz.")

    # Kelime eşleşmesine göre filtreleme
    matching_quotes = data[data['Kelimeler'].str.contains(input_phrase, case=False, na=False)]
    
    if not matching_quotes.empty:
        # Rastgele bir alıntı seçme
        random_index = random.choice(matching_quotes.index)
        selected_quote = matching_quotes.loc[random_index]
        return {
            "Title": selected_quote['Title'],
            "Author": selected_quote['Author'],
            "Text": selected_quote['Text']
        }
    else:
        return None

# Soruları döndüren fonksiyon
def display_questions():
    return [
        "1. Bu metin size ne ifade ediyor?",
        "2. Metindeki ana mesajı nasıl yorumlarsınız?",
        "3. Bu metnin günlük hayatınıza bir katkısı olabilir mi? Eğer evet, nasıl?"
    ]

# Endpoint: Alıntı döndürme
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
            raise HTTPException(status_code=404, detail="Eşleşen bir alıntı bulunamadı.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Ana endpoint (index.html'i döndürme)
@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = os.path.join(static_path, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html dosyası bulunamadı.")
    with open(index_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)