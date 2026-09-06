import uvicorn
from fastapi import FastAPI

from sqladmin import Admin, ModelView

from backend.database.db import engine
from backend.models import Post
from backend.routes.auth.Auth import router as authRouter
from backend.routes.Posts import router as postsRouter
from backend.routes.Users import router as usersRouter
from backend.routes.Comments import router as commentsRouter
from backend.routes.Likes import router as likesRouter
from backend.routes.Notifications import router as notificationsRouter

app = FastAPI()
admin = Admin(app, engine)

class PostsAdmin(ModelView, model=Post):
    column_list = [Post.id, Post.user_id, Post.content]

admin.add_view(PostsAdmin)

app.include_router(authRouter)
app.include_router(postsRouter)
app.include_router(usersRouter)
app.include_router(commentsRouter)
app.include_router(likesRouter)
app.include_router(notificationsRouter)

@app.get("/")
def welcome():
    return {"message": "Welcome"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
