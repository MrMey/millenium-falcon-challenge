class Config:
    """Configuration de base commune à tous les environnements."""
    LOG_LEVEL = "INFO"
    MILLENIUM_FALCON_PATH = "examples/example2/millennium-falcon.json"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(Config):
    LOG_LEVEL = "DEBUG"


config = {
    'development': DevelopmentConfig,
}