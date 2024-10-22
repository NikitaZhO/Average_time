from fastapi import UploadFile, HTTPException
import pandas as pd
import io
import logging


logger = logging.getLogger(__name__)


class FileController:
    def __init__(self, file: UploadFile):
        self.file = file

    async def read_file(self) -> pd.DataFrame:
        try:
            contents = await self.file.read()
            return self.parse_csv(contents)
        except Exception as e:
            logger.error(f"Ошибка чтения файла: {str(e)}")
            raise HTTPException(status_code=400, detail="Ошибка чтения файла")

    @staticmethod
    def parse_csv(contents: bytes) -> pd.DataFrame:
        try:
            decoded = contents.decode()
            return pd.read_csv(io.StringIO(decoded))
        except Exception as e:
            logger.error(f"Ошибка при чтении CSV: {str(e)}")
            raise HTTPException(status_code=400, detail="Невозможно прочитать CSV")

