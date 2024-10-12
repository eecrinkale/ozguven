from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from animeuse import get_closest_quote
from deep_translator import GoogleTranslator
import os

app = FastAPI(redoc_url=None)
app.mount("/static", StaticFiles(directory="web"), name="web")
templates = Jinja2Templates(directory="web")

# Initialize the limiter
limiter = Limiter(key_func=lambda request: request.query_params.get("key", ""))
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

script_path = os.path.dirname(os.path.realpath(__file__))

# Configure CORS to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/online")
async def check_online():
    return {"status": "online", "message": "Welcome to the API Service! 🌌"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/animequotes")
@limiter.limit("30/minute")
async def animequotes_bot(request: Request, msg: str = None, quote_type: str = None):
    if msg is None or quote_type is None:
        raise HTTPException(status_code=400, detail="Missing 'msg' or 'quote_type' parameter.")

    server_base_url = str(request.base_url)
    if not request.headers.get("Referer") or not request.headers["Referer"].startswith(server_base_url):
        raise HTTPException(status_code=403, detail="This endpoint is restricted. :)")

    response = await get_completion(msg)
    if quote_type.upper() == "TR":  # Make sure to convert to uppercase to match your condition
        translator = GoogleTranslator(source='en', target='tr')  # Assuming the translation from English to Turkish
        quote = extract_quote(response)
        if quote:
            translated_quote = translator.translate(quote)
            response = response.replace(quote, translated_quote)

    return {"message": response}

def extract_quote(response):
    start_quote = response.find("\"")
    end_quote = response.rfind("\"") if start_quote != -1 else -1
    if start_quote != -1 and end_quote != -1 and end_quote > start_quote:
        return response[start_quote + 1:end_quote]  # Extract the quote between the quotes
    return None

async def get_completion(user_input):
    response = get_closest_quote(user_input, n_responses=10)
    formatted_response = (
        f"Anime: {response['Anime']}\n"
        f"Character: {response['Character']}\n"
        f"Quote: \"{response['Quote']}\""
    )
    return formatted_response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)