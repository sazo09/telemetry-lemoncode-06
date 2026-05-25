# Servicng Static Files 

```py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Define API routes FIRST
@app.get("/api/hello")
async def hello():
    return {"message": "Hello from API"}

@app.get("/api/users")
async def get_users():
    return [{"id": 1, "name": "Alice"}]

# Mount static files at root LAST (serves index.html for SPA)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

```

## References

- https://fastapi.tiangolo.com/tutorial/static-files/