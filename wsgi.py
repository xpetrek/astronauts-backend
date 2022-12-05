from app import create_app
import os

os.system("python3 createdb.py")

app = create_app()