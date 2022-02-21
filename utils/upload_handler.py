import shutil

from fastapi import File
from fastapi import HTTPException
from pymongo.errors import PyMongoError
from sqlalchemy import true
from utils.db_connection import connection

class UploadHandler():

    def write_file_to_local(self,file:File):
        try:
            with open('uploads/'+file.filename,'wb') as filebuf:
                shutil.copyfileobj(file.file,filebuf)
        except shutil.Error as err :
            raise HTTPException(status_code=400,detail=err.args[0])
    
    def store_upload_details(self,upload_details:dict,user_data:dict)->bool:
        try:
            user_db=connection.fastapi_policyera.user.find_one({'email':user_data['email']})
            uploads=user_db.get('uploads',-1)
            if uploads==-1:
                user_db['uploads']=[]
                user_db['uploads'].append(upload_details)
            else:
                is_present=False
                for i in user_db['uploads']:
                    if upload_details['filename']==i['filename']:
                        is_present=True
                        break
                if not is_present:
                    user_db['uploads'].append(upload_details)
                
            connection.fastapi_policyera.user.update_one({'_id':user_db['_id']},{'$set':{'uploads':user_db['uploads']}},upsert=True)
        except PyMongoError as e:
            raise HTTPException(status_code=400,detail=e._message)
    
    def get_all_uploads(self,user_data):
        try:
            user_db=connection.fastapi_policyera.user.find_one({'email':user_data['email']})
            uploads=user_db['uploads']
            return uploads
        except PyMongoError as e:
            raise HTTPException(status_code=400,detail=e._message)

    
    

