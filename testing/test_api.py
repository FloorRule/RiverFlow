from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/test")
async def test_endpoint(req: Request):
    data = await req.json()
    return {"received": data, "message": "API success"}

@app.get("/health")
async def health():
    return {"status" : "ok"}
