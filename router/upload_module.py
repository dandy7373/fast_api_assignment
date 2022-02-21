from fastapi import APIRouter, UploadFile,File,Depends
from utils.upload_handler import UploadHandler
from utils.auth_handler import AuthHandler
from datetime import datetime

auth_handler=AuthHandler()
upload_router=APIRouter()

upload_handler=UploadHandler()

@upload_router.post('/upload')
async def upload_file(uploaded_file:UploadFile=File(...),user=Depends(auth_handler.token_auth)):
    upload_handler.write_file_to_local(uploaded_file)
    upload_handler.store_upload_details({'filename':uploaded_file.filename,'filetype':uploaded_file.content_type,'uploaded_at':datetime.now().timestamp()},user)
    return {'success':True,'message':'File Saved!'}

@upload_router.get('/upload')
async def get_uploads(user=Depends(auth_handler.token_auth)):
    uploads=upload_handler.get_all_uploads(user)
    return {'success':True,'uploads':uploads}