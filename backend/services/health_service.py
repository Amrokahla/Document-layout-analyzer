import os
import logging
from backend.core.config import settings

logger = logging.getLogger(__name__)

MODEL_DIR = settings.model_dir
MODEL_PATH = settings.classifier_model
VEC_PATH = settings.vectorizer


def check_liveness() -> dict:
    """Basic heartbeat — app is running."""
    logger.debug("Liveness check called")
    return {"status": "alive"}


def check_readiness() -> dict:
    """Deeper check — verify model/vectorizer exist."""
    logger.debug("Readiness check called")
    try:
        ready = os.path.exists(MODEL_PATH) and os.path.exists(VEC_PATH)
        status = "ready" if ready else "not ready"
        logger.info("Readiness check result: %s", status)
        return {
            "status": status,
            "model_path": MODEL_PATH,
            "vectorizer_path": VEC_PATH,
            "model_files_present": ready,
        }
    except Exception as e:
        logger.exception("Readiness check failed: %s", str(e))
        return {
            "status": "error",
            "error": str(e),
            "model_path": MODEL_PATH,
            "vectorizer_path": VEC_PATH,
            "model_files_present": False,
        }