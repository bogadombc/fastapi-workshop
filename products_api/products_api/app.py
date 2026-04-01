from fastapi import FastAPI

from products_api.routers.products import router as products_router

app = FastAPI()

app.include_router(products_router, prefix="/api/v1/products", tags=["Produtos"])


@app.get("/")
def read_root():
    return {"message": "Olá pequeno ponto azul!"}
