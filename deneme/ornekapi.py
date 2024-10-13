from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

@app.get("/", response_class=JSONResponse)
async def get_home(request: Request):
    return {"message": "Hello"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)