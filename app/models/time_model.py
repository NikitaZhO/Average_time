from pydantic import BaseModel


class DDoSAttackBase(BaseModel):
    saddr: str
    avg_dur: float

    class Config:
        from_attributes = True
