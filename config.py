# Import required libraries for:
# - environment variables, file path management, logging, and database configuration

import os, pathlib, logging
from dotenv import load_dotenv

# Load all variables from .env into the environment
load_dotenv()

INDUSTRY       = os.getenv("INDUSTRY",       "Healthcare")
LEARNER_SCHEMA = os.getenv("LEARNER_SCHEMA", "learner_29")

# Define project directories
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent
DATA_DIR     = PROJECT_ROOT / "data"
SQL_DIR      = PROJECT_ROOT / "sql"

# Create the data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# Output file location
RAW_DATA_PATH = DATA_DIR / "raw-data.csv"

DB_URL = os.getenv("DB_URL", "")

# Database connection
try:
    from sqlalchemy import create_engine
    if not DB_URL:
        raise ValueError("DB_URL not set. Check your .env file.")
    engine = create_engine(DB_URL, pool_pre_ping=True,
                           connect_args={"connect_timeout": 10})
    with engine.connect() as c:
        c.execute(__import__("sqlalchemy").text("SELECT 1"))
    DB_AVAILABLE = True

# If connection fails, disable database access
except Exception as e:
    engine       = None
    DB_AVAILABLE = False

# Configure application logger
def _setup_logger():
    lgr = logging.getLogger("module03")
    lgr.setLevel(logging.INFO)
    if not lgr.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        lgr.addHandler(h)
    return lgr

logger = _setup_logger()

if not DB_AVAILABLE:
    logger.warning("Database not connected. Check your .env file — DB_URL must be set.")
