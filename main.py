from typing import Optional
from typing import Union
from fastapi import FastAPI

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