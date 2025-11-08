import os
from backend import create_app

application = create_app(os.getenv("ENV", "development"))
