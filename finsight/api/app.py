"""Main FastAPI application."""

from fastapi import FastAPI
from finsight.api.webhooks import router as webhooks_router
from finsight.api.oauth import router as oauth_router

app = FastAPI(
    title="Finsight API",
    description="Financial Institution Connector API",
    version="0.1.0"
)

# Include routers
app.include_router(webhooks_router)
app.include_router(oauth_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Finsight API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
