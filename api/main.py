from fastapi import FastAPI

from api.routes import health, risk

app = FastAPI(title="Option Risk API", version="1.0.0")
app.include_router(health.router)
app.include_router(risk.router)
