import os
from backend.app import create_app

application = create_app(os.getenv("ENV", "development"))
