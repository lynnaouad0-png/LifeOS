from fastapi import FastAPI
from app.routers import (
    tasks, users, projects, goals, habits, 
    calendar, journals, reflections, skills, learning_resources,
    decisions, memories  # Added final strategic components
)
from app.core.database import Base, engine

# Ensure database tables are generated
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LifeOS API", version="1.0.0")

# Register routers
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(goals.router)
app.include_router(habits.router)
app.include_router(calendar.router)
app.include_router(journals.router)
app.include_router(reflections.router)
app.include_router(skills.router)
app.include_router(learning_resources.router)
app.include_router(decisions.router)  # Executed decision engine
app.include_router(memories.router)   # Executed memory engine

@app.get("/")
def root():
    return {"message": "Welcome to LifeOS Core API Engine"}