from fastapi import FastAPI
from src.utils.db import Base , engine 
from src.tasks.models  import TaskModel
from src.tasks.router  import task_routes
from src.user.router import user_routes
from src.frontend.router import router as frontend_router
from fastapi.staticfiles import StaticFiles
import mimetypes
import os
mimetypes.init()
mimetypes.add_type('text/css', '.css')
# when our application run then our application start connection in database 
# 
Base.metadata.create_all(engine)
app=FastAPI(title="This is my Task Management Applications")

from fastapi import Request, Response

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        import traceback
        return Response(content=f"Global Error: {str(e)}\n\n{traceback.format_exc()}", media_type="text/plain", status_code=500)

# Mount Static Files
# Here we change the static path to the dynamic path 
 # Fix for potential MIME type issues on Linux
mimetypes.add_type('text/css', '.css')

# Get absolute path
script_dir = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(script_dir, "static")

# Mount
app.mount("/static", StaticFiles(directory=static_path), name="static")

# app.mount("/static", StaticFiles(directory="static"), name="static")

# include routes are used to register the routes in the main routes 
app.include_router(frontend_router)
app.include_router(task_routes)
# Here we connect the userRoutes Here 
app.include_router(user_routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
