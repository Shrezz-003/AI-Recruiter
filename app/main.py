from fastapi import FastAPI
from app.core.config import settings
from app.api import auth, employee, employer
from app.db.base import Base, engine

# This will create the tables in the database if they don't exist
# Note: For production, you should use Alembic for migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(employee.router, prefix="/employee", tags=["Employee Tools"])
app.include_router(employer.router, prefix="/employer", tags=["Employer Tools"])

@app.get("/", tags=["Root"])
def read_root():
    return {"status": f"{settings.PROJECT_NAME} is running!"}