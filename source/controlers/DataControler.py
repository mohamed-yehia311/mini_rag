from .BaseControler import BaseControler
from fastapi import UploadFile
from models import ResponseSignal

class Datacontroler(BaseControler):
    def __init__(self):
        super().__init__()
    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.settings.FILE_MAX_SIZE * 1024 * 1024: # convert MB to bytes
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value
    

