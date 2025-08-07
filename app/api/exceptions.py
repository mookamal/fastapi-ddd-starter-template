from fastapi import status, Request
from fastapi.responses import JSONResponse


class DomainException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message}
    )


async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )