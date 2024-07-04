from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import RedirectResponse, JSONResponse
from fastapi_task_management.config.log_config import setup_logging
from fastapi_task_management.controller.task_controller import task_router

logger = setup_logging()
logger.info('Aplicação iniciada')

app = FastAPI(
    title="Gerenciador de Tarefas",
    description="API para gerenciamento de Tarefas",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=None,
    contact={
        "name": "Lucas Barbosa",
        "email": "lucasbdefanti@gmail.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Dev Server"
        }
    ]
)

app.include_router(task_router)

@app.exception_handler(Exception)
async def general_excep_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Erro inesperado"}
    )

@app.exception_handler(HTTPException)
async def general_excep_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

@app.get(path= '/', tags=['Redirect'], include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get(path= '/docs', tags=['Redirect'], include_in_schema=False)
async def get_openapi():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="OpenApi UI"
    )

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='localhost', port=8000)