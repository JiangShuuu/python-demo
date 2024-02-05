from typing import Optional, List, Union, Annotated
from fastapi import FastAPI, Query, Path
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
    descirption: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post('/items/')
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict

# **dict 繼承 class 設定格式, 並展平
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Optional[str] = None):
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
# ...代表required
@app.get("/items/required")
async def read_items_required(q: str = Query(default=..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
# 表示必須輸入值, 即便值為 None null
@app.get("/items/required/none")
async def read_items_required(q: Union[str, None] = Query(default=..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
# 查詢多個值
@app.get("/items/multi")
# q:Union[List[str], None] = Query(default=['foo', 'bar'])
# or
# q:list = Query(default=['foo', 'bar']) 該寫法不會檢查傳入型別
# title, description 文件註解
# deprecated 標註已棄用
# alias 別名參數
async def read_items_multi(
        q:Union[List[str], None] = Query(
        default=['foo', 'bar'],
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3)):
    query_items = {"q": q}
    return query_items


# Annotated & Path params & value valite
# https://fastapi.tiangolo.com/zh/tutorial/path-params-numeric-validations/#__tabbed_1_2
@app.get("/items/path/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[Union[str, None], Query(alias="item-query")] = None,  
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
