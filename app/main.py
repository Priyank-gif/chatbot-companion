# main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.controllers import pdf_controller, query_controller, url_processor, delete_vector_store, extend_vector_db

app = FastAPI()

@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")

app.include_router(pdf_controller.router)
app.include_router(query_controller.router)
app.include_router(url_processor.router)
app.include_router(delete_vector_store.router)
app.include_router(extend_vector_db.router)
