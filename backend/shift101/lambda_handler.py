"""AWS Lambda adapter for Shift101 FastAPI."""
from mangum import Mangum
from .main import app
handler = Mangum(app, lifespan="off")
