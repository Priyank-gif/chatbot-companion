# main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from app.controllers import pdf_controller, query_controller, url_processor, delete_vector_store, extend_vector_db, \
    chat_controllers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods like GET, POST, DELETE
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(pdf_controller.router)
app.include_router(query_controller.router)
app.include_router(url_processor.router)
app.include_router(delete_vector_store.router)
app.include_router(extend_vector_db.router)
app.include_router(chat_controllers.router)
