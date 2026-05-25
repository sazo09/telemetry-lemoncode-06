# Fast API

## Virtual Environment

```bash
mkdir map-api
cd map-api
```

```bash
python -m venv .venv
```

```bash 
source .venv/bin/activate
```

```bash
which python
```

```bash
python -m pip install --upgrade pip
```

```bash
python -m ensurepip --upgrade
```

## Install Dependencies

```bash
pip install "fastapi[standard]"
```

Dump `requirements.txt`

```bash
pip freeze > requirements.txt
```

## Scaffoling the Project

```bash
touch __init__.py main.py
```

```bash
mkdir api schemas
touch api/__init__.py api/endpoints.py
touch schemas/__init__.py schemas/item.py
```

## Creating the API Endpoint

Create `app-map/schemas/item.py`

```py
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

Create `app-map/api/endpoints.py`

```py
from fastapi import APIRouter

router = APIRouter()

@router.get("/api/items/")
async def get_items():
    items = [
        {"name": "Foo1", "description": None, "price": "12", "tax": None},
        {"name": "Foo2", "description": None, "price": "13", "tax": None},
        {"name": "Foo3", "description": None, "price": "15", "tax": None}
    ]
    return items

```

Create `app-map/main.py`

```py
from fastapi import FastAPI 
from api.endpoints import router as item_router

app = FastAPI()

app.include_router(item_router)

```

```bash
fastapi dev main.py
```

## References

- https://docs.pydantic.dev/latest/