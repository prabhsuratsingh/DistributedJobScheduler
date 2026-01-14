from fastapi import Depends, FastAPI, HTTPException
import redis
import redis.exceptions
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from app.core.queue import redis_client
from app.database import db
from app.api.jobs import router as job_router

app = FastAPI()

@app.get("/health")
async def health():
    return {"Status": "healthy"}

@app.get("/health/redis")
async def health_redis():
    try:
        redis_client.ping()
        return {"Status": "healthy"} 
    except redis.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail={
            "Redis": "Unhealthy",
            "Error": redis.exceptions.ConnectionError.__name__
        })

@app.get("/health/postgres")
async def health_postgres(db: Session = Depends(db.get_db)):
    try:
        db.execute(text("SELECT 1"))
        db.close()
        return {"Postgres": "Healthy"}
    except OperationalError:
        raise HTTPException(status_code=500, detail={
            "Postgres": "Unhealthy",
            "Error": OperationalError.__name__
        })

app.include_router(job_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)