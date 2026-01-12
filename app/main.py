from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"Status": "healthy"}

@app.get("/health/redis")
async def health_redis():
    pass

@app.get("/health/postgres")
async def health_postgres():
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)