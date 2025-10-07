from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import dashboard_router, transactions_router

app = FastAPI(
    title="Finsight API",
    description="Financial insights and transaction management API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard_router)
app.include_router(transactions_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Finsight API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
