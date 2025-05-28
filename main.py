from fastapi import FastAPI, Request
import subprocess

app = FastAPI()

@app.post("/upload")
async def upload(request: Request):
    body = await request.json()
    proxy = body["proxy"]
    cookies = body["cookies_path"]

    result = subprocess.run(
        ["python3", "upload_to_tiktok.py", cookies, proxy],
        capture_output=True,
        text=True
    )
    return {"stdout": result.stdout, "stderr": result.stderr}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
