from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Configuration de base commune à tous les environnements."""

    LOG_LEVEL = "INFO"
    MILLENIUM_FALCON_PATH = (
        BASE_DIR / "examples" / "example2" / "millennium-falcon.json"
    )


class DevelopmentConfig(Config):
    LOG_LEVEL = "DEBUG"
    FRONTEND_URL = "http://localhost:4200"


class ProdConfig(Config):
    LOG_LEVEL = "INFO"


config = {"development": DevelopmentConfig, "production": ProdConfig}
