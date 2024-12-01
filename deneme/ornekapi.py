from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

@app.get("/", response_class=JSONResponse)
async def get_home(request: Request):
    return {"message": "Hello"}

@app.get("/naber", response_class=JSONResponse)
async def get_home(request: Request):
    return {"message": "Naber"}

# New route to take a number (sayi) and return sayi + 1000
@app.get("/f1/{sayi}", response_class=JSONResponse)
async def add_number(sayi: int):
    if sayi < 10:
        return {"result": "Sayı Cok küçük"}
    result = sayi + 1000
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
