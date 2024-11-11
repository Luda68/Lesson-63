# from fastapi import FastAPI
#
# app  = FastAPI()
#
#
# @app.get("/")
# async def welcome():
#     return {'message': 'Главная страница'}
#
#
# @app.get('/user/admin')
# async def admin():
#     return {'message': 'Вы вошли как администратор'}
#
#
# @app.get('/user/{user_id}')
# async def user(user_id):
#     return {'message': f'Вы вошли как пользователь №{user_id}'}
#
#
# @app.get('/user')
# async def user_info(username, age):
#     return f'Информация о пользователе, Имя: {username}, Возраст: {age}'

#
# from fastapi import FastAPI, Path
# from typing import Annotated
#
# app = FastAPI()
#
#
# @app.get('/')
# async def welcome() -> str:
#     return (f'Главная страница')
#
#
# @app.get('/user/admin')
# async def administrator() -> str:
#     return (f'Вы вошли как администратор')
#
#
# @app.get('/user/{user_id}')
# async def user_number(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')]):
#     return (f'Вы вошли как пользователь № {user_id}')
#
#
# @app.get('/user/{username}/{age}')
# async def user_info(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
#                     age: Annotated[int, Path(ge=18, le=120, description='Enter age')]):
#     return (f'Информация о пользователе. Имя: {username}, Возраст: {age}')


#
# from fastapi import FastAPI, Path
# from typing import Annotated
#
#
# app = FastAPI()
#
# users = {'1': 'Имя: Example, возраст: 18'}
#
# @app.get('/users')
# async def get_users() -> dict:
#     return users
#
# @app.post('/user/{username}/{age}')
# async def create_user(username: Annotated[str, Path(min_length=3, max_length=15, description='Введите Ваше имя', example=' Сергей')]
#                       , age: int) -> str:
#     current_index = str(int(max(users, key=int)) + 1)
#     users[current_index] = username, age
#     return f'Пользователь {current_index} зарегистрирован!'
#
# @app.put('/user/{user_id}/{username}/{age}')
# async def update_user(user_id: str = Path(ge=1, le=100, description='Введите возраст', example= '1')
#                       , username: str =Path(min_length=3, max_length=20, description=' Введите Ваше имя', example= 'Сергей')
#                       , age: int = 30) -> str:
#     users[user_id] = user_id, username, age
#     return f'Информация о пользователе id# {user_id} обновлена'
#
# @app.delete('/user/{user_id}')
# async def delite_user(user_id: str) -> str:
#     users.pop(user_id)
#     return f'Пользователь {user_id} удалён'


from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

users = []

class User(BaseModel):
    id: int  # номер пользователя(int)
    username: str  #имя пользователя(str)
    age: int  #возраст пользователя (int)

@app.get(path='/users')
async def get_message() -> list[User]:
    return users

@app.post(path='/user/{username}/{age}')
async def post_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                    age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> User:
    new_id = (users[-1].id + 1) if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put(path='/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    else:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete(path='/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')]) -> User:
    for i, user in enumerate(users):
        if user.id == user_id:
            return users.pop(i)
    else:
        raise HTTPException(status_code=404, detail='User was not found')


