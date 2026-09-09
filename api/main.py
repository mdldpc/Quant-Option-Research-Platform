from fastapi import FastAPI

from api.routes import health, risk
from api.routes import valuation

app = FastAPI(title="Option Risk API", version="1.0.0")
app.include_router(health.router)
app.include_router(risk.router)
app.include_router(valuation.router)
