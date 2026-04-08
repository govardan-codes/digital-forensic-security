import logging

logger = logging.getLogger("forensic_app.utils")

def mask_secret(s: str, keep: int = 3) -> str:
    """Mask a secret string leaving last `keep` characters visible.
       If secret is None or empty returns '<empty>'.
    """
    if not s:
        return "<empty>"
    if len(s) <= keep:
        return "*" * len(s)
    return "*" * (len(s) - keep) + s[-keep:]

def log_db_error(logger, exc):
    logger.exception("Database error: %s", exc)
