from fastapi import FastAPI

app = FastAPI(title = "InsightAPI")

@app.get("/health")
def health_check():
    return {"status":"healthy"}

