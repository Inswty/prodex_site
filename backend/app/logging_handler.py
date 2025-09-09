import logging
from datetime import datetime, timezone

from .models import db, Log


class DBHandler(logging.Handler):
    """Лог-хендлер, сохраняет записи в базу данных."""
    def emit(self, record):
        log = Log(
            created_at=datetime.now(timezone.utc),
            level=record.levelname,
            message=record.getMessage(),
            logger_name=record.name
        )
        db.session.add(log)
        db.session.commit()
