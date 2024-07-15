from mangum import Mangum
from lib.main import app

handler = Mangum(app)
