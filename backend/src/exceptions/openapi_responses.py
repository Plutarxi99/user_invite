from backend.src.exceptions.schemas import ErrorResponseSchema
from backend.src.apps.user.schemas import CurrentUserResponseModel, UpdateUserResponseModel

# Дополнительные ответы для отображения в openapi
def responses_error(
        code: int, message: str
):
    return {code: {"model": ErrorResponseSchema, "descriptions": f"{message}",
                   "content": {
                       "application/json": {
                           "example": {
                               "code": code, "message": f"{message}"
                           }
                       }
                   }
                   }}


get_cur_user_resp_200 = {200: {"model": CurrentUserResponseModel,
                               "description": "Вход пользователя",
                               "content": {
                                   "application/json": {
                                       "example": {
                                           "first_name": "string",
                                           "last_name": "string",
                                           "other_name": "string",
                                           "email": "string@string.ru",
                                           "phone": "8 952 777 77 77",
                                           "birthday": "07.10.1952",
                                           "is_admin": False,

                                       }
                                   }}
                               }}

update_cur_user_resp_200 = {200: {"model": UpdateUserResponseModel,
                                  "description": "Вход пользователя",
                                  "content": {
                                      "application/json": {
                                          "example": {
                                              "id": 0,
                                              "first_name": "string",
                                              "last_name": "string",
                                              "other_name": "string",
                                              "email": "string@string.ru",
                                              "phone": "8 952 777 77 77",
                                              "birthday": "07.10.1952"

                                          }
                                      }}
                                  }}

user_not_auth_401 = {401: {"model": ErrorResponseSchema,
                           "description": "Вход пользователя",
                           "content": {
                               "application/json": {
                                   "example": {
                                       "code": 401,
                                       "last_name": "Пользователь не авторизован"

                                   }
                               }}
                           }}

responses_not_found_404 = {
    **responses_error(code=404, message="Не существует такого пользователя в системе"),
}