import shutil

from fastapi import APIRouter, HTTPException
import os

from app.config import vector_db_path

router = APIRouter(tags=['delete vector db'])


@router.delete("/delete-vector-store/")
async def delete_vector_store():
    try:
        if os.path.exists(vector_db_path):
            print('path exists')
            shutil.rmtree(vector_db_path, ignore_errors=True)
            return {"message": "Vector store successfully deleted"}
        else:
            raise HTTPException(status_code=404, detail="Vector store file not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied: Unable to access the file or directory. Check the application's permissions.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

