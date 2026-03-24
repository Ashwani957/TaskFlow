from fastapi import FastAPI
from src.utils.db import Base , engine 
from src.tasks.models  import TaskModel
from src.tasks.router  import task_routes
from src.user.router import user_routes
from src.frontend.router import router as frontend_router
from fastapi.staticfiles import StaticFiles

# when our application run then our application start connection in database 
# 
Base.metadata.create_all(engine)
app=FastAPI(title="This is my Task Management Applications")

# Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# include routes are used to register the routes in the main routes 
app.include_router(frontend_router)
app.include_router(task_routes)
# Here we connect the userRoutes Here 
app.include_router(user_routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)