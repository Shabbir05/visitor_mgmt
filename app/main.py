from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, users, visitors, approvals, visits
from fastapi.middleware.cors import CORSMiddleware


# Create FastAPI instance
app = FastAPI(title="Visitor Management System", version="1.0")

# Allow CORS for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(visitors.router, prefix="/visitors", tags=["Visitors"])
app.include_router(approvals.router, prefix="/approvals", tags=["Approvals"])
app.include_router(visits.router, prefix="/visits", tags=["Visits"])

# Test endpoint
@app.get("/")
def root():
    return {"message": "Visitor Management System API running 🚀"}
