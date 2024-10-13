from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import random
from quote import get_closest_quote  # Assuming you have this function in quote.py

# Initialize FastAPI app
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template rendering setup (HTML)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/zivir", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("zivir.html", {"request": request})

@app.post("/get_quote/")
async def get_quote(message: str = Form(...)):
    if not message:
        raise HTTPException(status_code=400, detail="No message provided")
    
    # Call get_closest_quote function from quote.py
    closest_quote = get_closest_quote(message, n_responses=10)
    
    return {
        "anime": closest_quote['Anime'],
        "character": closest_quote['Character'],
        "quote": closest_quote['Quote']
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
