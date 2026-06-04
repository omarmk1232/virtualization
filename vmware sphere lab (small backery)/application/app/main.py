from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.routers import products, orders
import app.models as models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MokTech Bakery",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/menu")
async def menu(request: Request, db: Session = Depends(get_db)):
    from app import crud
    product_list = crud.get_products(db, available_only=True)
    return templates.TemplateResponse("menu.html", {"request": request, "products": product_list})


@app.get("/order")
async def order_page(request: Request):
    return templates.TemplateResponse("order.html", {"request": request})


@app.get("/admin/orders")
async def admin_orders(request: Request, db: Session = Depends(get_db)):
    from app import crud
    order_list = crud.get_orders(db)
    return templates.TemplateResponse("orders_admin.html", {"request": request, "orders": order_list})
