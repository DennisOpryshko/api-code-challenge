from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from driver import run_search
from datatypes import SearchResponse
from wikipedia import PageError, DisambiguationError, HTTPTimeoutError, RedirectError


app = FastAPI()


@app.exception_handler(PageError)
async def page_not_found(req: Request, exc: PageError):
    return JSONResponse(
        status_code=404,
        content=exc.__str__()
    )


@app.exception_handler(DisambiguationError)
async def unexpected_disambiguation(req: Request, exc: DisambiguationError):
    return JSONResponse(
        status_code=500,
        content="Recursive disambiguation page (possibly wikipedia error)."
    )


@app.exception_handler(HTTPTimeoutError)
async def http_timeout(req: Request, exc: HTTPTimeoutError):
    return JSONResponse(
        status_code=504,
        content=f"[{exc.query}] resulted in a timeout"
    )


@app.exception_handler(RedirectError)
async def unexpected_redirect(req: Request, exc: RedirectError):
    return JSONResponse(
        status_code=500,
        content=f"Unexpectedly redirected for [{exc.title}]"
    )


@app.get("/search/{search_string}", response_model=SearchResponse)
async def search(search_string: str, top: int):
    return run_search(search_string, top)

