import os
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from ..config import settings
from PIL import Image
import io

class FileService:
    ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    ALLOWED_DOC_TYPES = ["application/pdf", "application/msword", 
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    
    @staticmethod
    async def save_upload_file(file: UploadFile, user_id: int) -> str:
        """Save uploaded file and return the file path"""
        
        #validate file size
        contents = await file.read()
        if len(contents) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        #validate file type
        file_type = file.content_type
        if file_type not in FileService.ALLOWED_DOC_TYPES + FileService.ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="File type not allowed")
        
        #create upload dir if not exist
        upload_dir = os.path.join(settings.UPLOAD_DIR, str(user_id))
        os.makedirs(upload_dir, exist_ok=True)

        #generate uniqe filena  
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)

        #save file
        with open(file_path, "wb") as f:
            f.write(contents)
        
        #create thumbnail if have image
        if file_type in FileService.ALLOWED_IMAGE_TYPES:
            FileService._create_thumbnail(file_path, upload_dir)
        
        return file_path
    
    @staticmethod
    def _create_thumbnail(image_path: str, upload_dir: str) -> Optional[str]:
        """Create thumbnail for image"""
        try:
            img = Image.open(image_path)
            img.thumbnail((300, 300))

            filename = os.path.basename(image_path)
            thumb_filename = f"thumb_{filename}"
            thumb_path = os.path.join(upload_dir, thumb_filename)

            img.save(thumb_path)
            return thumb_path
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return None
        
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Delete a file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                #also deletet thubm
                dir_path = os.path.dirname(file_path)
                filename = os.path.basename(file_path)
                thumb_path = os.path.join(dir_path, f"thumb_{filename}")
                if os.path.exists(thumb_path):
                    os.remove(thumb_path)

                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    @staticmethod 
    def get_file_url(file_path: str) -> str:
        """Convert file path to URL"""
        return f"/upload/{file_path.replace(settings.UPLOAD_DIR + '/', '')}"
    
file_service = FileService()