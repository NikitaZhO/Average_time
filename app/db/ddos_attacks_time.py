from sqlalchemy import Column, Integer, String, Float
from app.db import Base


class DDoSAttack(Base):
    __tablename__ = "ddos_attacks_time"

    id = Column(Integer, primary_key=True, index=True)
    saddr = Column(String, index=True)
    avg_dur = Column(Float)
