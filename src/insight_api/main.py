from fastapi import FastAPI

from insight_api.api.routes import router

app = FastAPI(title = "InsightAPI")

app.include_router(router)