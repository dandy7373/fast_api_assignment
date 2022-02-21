from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError
from models.signin import SigninModel
from models.signup import SignUpModel
from utils.db_connection import connection
from utils.auth_handler import AuthHandler


authenticationRouter = APIRouter()

auth_handler = AuthHandler()


@authenticationRouter.post('/signup')
async def signup(user: SignUpModel):
    user.password = auth_handler.get_hashed_password(user.password)
    signup_result=auth_handler.create_user(user)
    if signup_result:
        return {'success':True,'access_token':signup_result}
    

@authenticationRouter.post('/sigin')
async def sigin(user: SigninModel):
    token=auth_handler.login_user(user)
    return {'success':True,'access_token':token}
