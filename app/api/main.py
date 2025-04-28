from fastapi import APIRouter

from app.api.routes import cocktail, ingredient, main

app_router = APIRouter()
app_router.include_router(cocktail.router, prefix="/cocktails", tags=["cocktails"])
app_router.include_router(main.router, tags=["main"])
app_router.include_router(
    ingredient.router, prefix="/ingredients", tags=["ingredients"]
)
