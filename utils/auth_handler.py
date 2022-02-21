from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
import jwt
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os
from pymongo.errors import PyMongoError
from models.signin import SigninModel
from models.signup import SignUpModel
from utils.db_connection import connection
from utils.email_validator import validate_email

class AuthHandler():
    bearer=HTTPBearer()
    load_dotenv()
    JWT_SECRET=os.getenv("SECRET")
    JWT_ALGORITHM=os.getenv("ALGORITHM")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    def generate_token(self, payload:dict):
        
        expire_time=datetime.now()+timedelta(minutes=2)
        payload['expiry']=expire_time.timestamp()
        token=jwt.encode(payload,self.JWT_SECRET,algorithm=self.JWT_ALGORITHM)
        return token
    
    def decode_token(self,token):
        try:
            user_data=jwt.decode(token,self.JWT_SECRET,algorithms=self.JWT_ALGORITHM)
            return user_data
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=400,detail=e.args[0])
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=400,detail=e.args[0])
        
    def get_hashed_password(self,password):
        return self.pwd_context.hash(password)

    def verify_password(self,password,hashed_password):
        return self.pwd_context.verify(password,hashed_password)

    #signup helper for user
    def create_user(self, user_data:SignUpModel):
        try:
            if not validate_email(user_data.email):
                raise HTTPException(status_code=400,detail='Invalid email address')
            user_check = connection.fastapi_policyera.user.find_one(
            {'email': user_data.email})
            if user_check:
                raise HTTPException(status_code=400,detail='User with given email already exists!')
            connection.fastapi_policyera.user.insert_one(user_data.dict())

            payload=user_data.dict()
            del payload['re_type_password']

            return self.generate_token(payload)

        except PyMongoError as e:
            raise HTTPException(status_code=400,detail=e._message)
    
    #sigin helper for user
    def login_user(self,login_data:SigninModel)->str:
        try:
            userData = connection.fastapi_policyera.user.find_one(
            {'email': login_data.email}) 
            if userData:
                if self.verify_password(login_data.password,userData["password"]):
                    return self.generate_token(login_data.dict())
            
            raise HTTPException(
                status_code=400, detail='Incorrect password/User doesn\'t exist')
        except PyMongoError as e:
            raise HTTPException(status_code=400,detail=e._message)
    
    #bearer toke handler
    def token_auth(self, auth:HTTPAuthorizationCredentials=Security(bearer)):
        return self.decode_token(auth.credentials)

        