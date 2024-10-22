from fastapi import UploadFile, Form, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import logging
from app.controllers.file_controller import FileController
from app.controllers.db_controller import CheckingData
from app.db import get_db

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/uploadfile")
async def upload_csv(file: UploadFile = Form(...), db: Session = Depends(get_db)) -> list:
    logger.info("Началась обработка файла")

    csv_handler = FileController(file)
    data_processor = CheckingData(db)

    try:
        df = await csv_handler.read_file()
        data_processor.process(df)
        return data_processor.fetch_all_attacks()
    except ValueError as e:
        logger.error(f"Ошибка в запросе /uploadfile - {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
