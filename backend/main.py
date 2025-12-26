import threading
import time
import uvicorn
from API_server import app
from db.init_db_script import init_db

def start_fastapi():
    #init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)

print("FastAPI are running...")
start_fastapi()