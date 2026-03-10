from fastapi import FastAPI
from api.auth.route import router as auth_router
from api.tasks.routes import router as task_router
from api.reports.routes import router as reports_router
from api.database.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo List API", version="1.0.0")

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(reports_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Todo List API"}