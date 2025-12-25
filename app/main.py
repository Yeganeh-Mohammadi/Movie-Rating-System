from fastapi import FastAPI

app = FastAPI(title="Movie Rating System API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Movie Rating System Phase 1"}