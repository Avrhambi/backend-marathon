from fastapi import FastAPI
from enum import Enum


app = FastAPI()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
async def root():
    return {"message": "Hello World"}


# path parameter with type validation
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


# path parameter with limited values validation
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# path parameter containing a path
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# Query Parameters with type validation
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# path parameters and Query Parameters
@app.get("/posts/{post_id}")
async def read_post(post_id: str, q: str | None = None, short: bool = False):
    post = {"post_id": post_id}
    if q:
        post.update({"q": q})
    if not short:
        post.update(
            {"description": "This is an amazing post that has a long description"}
        )
    return post