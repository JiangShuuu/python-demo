from typing import Optional
from typing import Union
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI() # 建立一個 Fast API application

@app.get("/") # 指定 api 路徑 (get方法)
def read_root():
    """ 第一個:api """ # 文件註解
    return {"Hello": "World"}


@app.get("/users/{user_id}") # 指定 api 路徑 (get方法)
def read_user(user_id: int, q: Optional[str] = None):
    return {"user_id": user_id, "q": q}

@app.get("/get_number/{number}") 
async def read_number(number: int):
    return {"number": number}

# Query Parameter
@app.get("/query_param_str") 
async def query_param_str(pID: str): # 轉換成字串
    return {"user": pID}

@app.get("/query_param_int")
async def query_param_int(pID: int): # 轉換成整數
    return {"user": pID}

# 預設值
@app.get("/default_param")
async def query_param_str(param_a: str, param_b: str="example"): # 轉換成字串
    return {"param_a": param_a, "param_b": param_b}

# 選擇性參數 Optional[str] 與 Union[str, None] 是完全等價的, 可以不輸入值, 但 key 要在
@app.get("/optional_union")
def optional_example(user_name:str, gender: Union[str, None]):
    return {"user_name": user_name, "gender": gender}

@app.get("/optional_optional")
def optional_example(user_name:str, gender: Optional[str]):
    return {"user_name": user_name, "gender": gender}

# baseModel
# https://fastapi.tiangolo.com/zh/tutorial/body/

class Item(BaseModel):
    name: str
    descirption: str | None = None
    price: float
    tax: float | None = None

@app.post('/items/')
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict

# **dict 繼承 class 設定格式, 並展平
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if (q):
        result.update({"q": q})
    return {
        "success": True,
        "result": result
    }

# search params & validate
# https://fastapi.tiangolo.com/zh/tutorial/query-params-str-validations/
@app.get("/items/")
# 可加入正規表達式作為驗證工具之一
async def read_items(q: Union[str, None] = Query(
    default=None, min_length=3,  max_length=50, pattern="^fixedquery$"
    )):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

