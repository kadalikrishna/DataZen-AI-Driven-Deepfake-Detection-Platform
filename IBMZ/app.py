"""Deployment entry point for the canonical DataZen application."""
import os
from backend.app import app
application=app
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT","5000")),debug=False)
