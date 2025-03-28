import streamlit as st
import sys
import os
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.app import main

if __name__ == "__main__":
    main()
