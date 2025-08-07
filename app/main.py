from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.v1.router import api_router
from app.api.exceptions import domain_exception_handler, value_error_handler, DomainException


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG,
    )
    
    # Add CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    application.include_router(api_router, prefix=settings.API_V1_PREFIX)
    
    # Add exception handlers
    application.add_exception_handler(DomainException, domain_exception_handler)
    application.add_exception_handler(ValueError, value_error_handler)
    
    return application


app = create_application()


@app.get("/")
async def root():
    return {"message": "FastAPI DDD Project", "version": settings.VERSION}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )