# ensure project root is on sys.path for imports like `from main import app`
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
