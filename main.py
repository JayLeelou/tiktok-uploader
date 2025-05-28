from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/upload")
async def upload(request: Request):
    return {"message": "✅ FastAPI route is working!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0"
