#!/usr/bin/env python3
"""
This is the WSGI entry point for the application
"""
import os
import sys

# Configure Flask environment variables
os.environ['FLASK_APP'] = 'wsgi.py'
os.environ['FLASK_ENV'] = 'development'

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import app

if __name__ == "__main__":
    app.run() 