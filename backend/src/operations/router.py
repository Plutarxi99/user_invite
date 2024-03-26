from fastapi import APIRouter

from backend.src.apps.auth.endpoints import router_auth
from backend.src.apps.register.endpoints import router_register
from backend.src.apps.user.endpoints import router_user
from backend.src.apps.referel.endpoints import router_referal

# соединения эндпоинтов для включения их в сервис
api_router = APIRouter()
api_router.include_router(router_auth,
                          tags=['auth'])
api_router.include_router(router_user, prefix="/users",
                          tags=["users"])
api_router.include_router(router_register, prefix="/register",
                          tags=['register'])
api_router.include_router(router_referal, prefix="/referal",
                          tags=['referal'])
