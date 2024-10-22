from fastapi import UploadFile, Form, APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import pandas as pd
import io
import logging
from app.models.time_model import DDoSAttackBase
from app.db.ddos_attacks_time import DDoSAttack
from app.db import get_db

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/uploadfile")
async def upload_csv(file: UploadFile = Form(...), db: Session = Depends(get_db)) -> list:
    logger.info("Началась обработка файла")
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode()))

        for _, group in df.groupby("saddr"):
            saddr = group["saddr"].iloc[0]
            avg_dur = group["dur"].mean()

            db_attack = db.query(DDoSAttack).filter(DDoSAttack.saddr == saddr).first()
            if db_attack:
                db_attack.avg_dur = (db_attack.avg_dur + avg_dur) / 2
            else:
                db_attack = DDoSAttack(saddr=saddr, avg_dur=avg_dur)
                db.add(db_attack)

            db.commit()

        response = db.query(DDoSAttack).all()
        return [DDoSAttackBase.from_orm(item).dict() for item in response]
    except Exception as e:
        logger.error(f"Ошибка обработки файла: {str(e)}")
        raise HTTPException(status_code=400, detail="Ошибка обработки файла")
