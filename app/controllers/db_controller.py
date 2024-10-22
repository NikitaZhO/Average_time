from sqlalchemy.orm import Session
from fastapi import HTTPException
import pandas as pd
import logging
from app.models.time_model import DDoSAttackBase
from app.db.ddos_attacks_time import DDoSAttack


logger = logging.getLogger(__name__)


class CheckingData:
    def __init__(self, db: Session):
        self.db = db

    def process(self, df: pd.DataFrame):
        try:
            for _, group in df.groupby("saddr"):
                saddr = group["saddr"].iloc[0]
                avg_dur = group["dur"].mean()

                db_attack = self.db.query(DDoSAttack).filter(DDoSAttack.saddr == saddr).first()
                if db_attack:
                    db_attack.avg_dur = (db_attack.avg_dur + avg_dur) / 2
                else:
                    db_attack = DDoSAttack(saddr=saddr, avg_dur=avg_dur)
                    self.db.add(db_attack)

                self.db.commit()
        except Exception as e:
            logger.error(f"Ошибка обработки данных: {str(e)}")
            raise HTTPException(status_code=400, detail="Ошибка обработки данных")

    def fetch_all_attacks(self) -> list:
        try:
            response = self.db.query(DDoSAttack).all()
            return [DDoSAttackBase.from_orm(item).dict() for item in response]
        except Exception as e:
            logger.error(f"Ошибка получения данных: {str(e)}")
            raise HTTPException(status_code=400, detail="Ошибка получения данных")
