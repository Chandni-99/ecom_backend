from fastapi import FastAPI
from fastapi.openapi.models import SecurityScheme
from fastapi.openapi.utils import get_openapi
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

from app.db.base_class import engine, Base
from app.routers import products, categories, users, auth, carts,reviews

app =FastAPI()
limiter = Limiter(key_func=get_remote_address)

# Apply the limiter as a middleware
app.state.limiter = limiter

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="User CRUD API",
        version="1.0.0",
        description="API for CRUD operation for user, authentication,login, register,forgot password",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: <strong>'Bearer &lt;JWT&gt;'</strong>, where JWT is the access token"
        }
    }
    # Don't apply security globally
    # openapi_schema["security"] = [{"Bearer Auth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(carts.router)
app.include_router(reviews.router)

@app.exception_handler(429)
async def rate_limit_exceeded_handler(request,exc):
    return JSONResponse(
        status_code=429,
        content={"detail":"timeout expired, please try again later."}
    )