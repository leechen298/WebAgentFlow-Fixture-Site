from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.schemas import ApiErrorResponse
from app.validation_api import router as validation_api_router

app = FastAPI(
    title="WebAgentFlow Fixture Site API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(validation_api_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(HTTPException)
async def handle_http_exception(_: Request, exc: HTTPException) -> JSONResponse:
    message = exc.detail if isinstance(exc.detail, str) else "Request failed."
    data = exc.detail if isinstance(exc.detail, (dict, list)) else None
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiErrorResponse(code=exc.status_code, msg=message, data=data).model_dump(),
    )


def format_validation_error_message(errors: list[dict]) -> str:
    if not errors:
        return "Validation error."

    first_error = errors[0]
    loc = first_error.get("loc", [])
    msg = first_error.get("msg", "Invalid value")
    loc_str = ".".join(str(x) for x in loc if x != "body") if loc else "field"

    if len(errors) == 1:
        return f"{loc_str}: {msg}"
    return f"{loc_str}: {msg} (and {len(errors) - 1} more errors)"


@app.exception_handler(RequestValidationError)
async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    message = format_validation_error_message(errors)
    return JSONResponse(
        status_code=422,
        content=ApiErrorResponse(code=422, msg=message, data=errors).model_dump(),
    )
