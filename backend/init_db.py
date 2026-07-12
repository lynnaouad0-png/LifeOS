from app.core.database import engine, Base
from app.models.models import User, Goal, Project, Task, CalendarEvent, Habit, Journal, Reflection, Skill, LearningResource, Decision, Memory

print("Connecting to the database and creating tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("🎉 Success! Your LifeOS database tables have been created.")
except Exception as e:
    print(f"❌ Error creating database tables: {e}")