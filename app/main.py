from config import app
from routers.notes import router as notes_router
from routers.tags import router as tags_router

app.include_router(notes_router)
app.include_router(tags_router)

