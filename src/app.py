from fastapi import FastAPI, security
import logging
from fastapi.responses import JSONResponse
import uvicorn

# Project Library
from routes.user import router as users_router
from routes.book import router as book_router

app = FastAPI()
logger = logging.getLogger(__name__)


@app.get("/api/v1/health-check")
def health_check():
    logger.info("Health check API is working")
    return JSONResponse(
        status_code=200,
        content={
            "status": True,
            "data": None,
            "message": "Up and running",
        },
    )


app.include_router(users_router, tags=["Users"], prefix="/api/v1/users")
app.include_router(book_router, tags=["Book"], prefix="/api/v1/book")

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, env_file=".env")
