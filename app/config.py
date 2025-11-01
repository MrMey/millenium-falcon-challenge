class Config:
    """Configuration de base commune à tous les environnements."""
    LOG_LEVEL = "INFO"
    MILLENIUM_FALCON_PATH = r"C:\Users\Moi\Documents\projects\millenium-falcon-challenge\examples\example2\millennium-falcon.json"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(Config):
    LOG_LEVEL = "DEBUG"


config = {
    'development': DevelopmentConfig,
}