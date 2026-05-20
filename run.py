# ================================================================
# run.py — Healthcare SQL Project Entry Point
# ================================================================
# python run.py
#
# WHAT HAPPENS:
#   1. Demonstrates SQL concepts in terminal
#   2. Runs final extraction query
#   3. Saves data/raw-data.csv
# ================================================================

import sys, pathlib
_root = pathlib.Path(__file__).resolve().parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from config import INDUSTRY, DB_AVAILABLE, logger
from src.querry_runner  import SQLQueryRunner
from src.data_extractor import DataExtractor

def main() -> None:

    logger.info("=" * 60)
    logger.info("  HEALTHCARE SQL PROJECT")
    logger.info(f"  Industry: {INDUSTRY}")
    logger.info(f"  DB Available: {DB_AVAILABLE}")
    logger.info("=" * 60)

# ============================================================
    # PART 1 — SQL DEMONSTRATIONS
# =============================================================

    runner = SQLQueryRunner()

    print("\n── DEMO 1: Basic selected Queries")
    runner.demo_basics()

    print("\n── DEMO 2: Aggregation Queries")
    runner.demo_aggregation()

    print("\n── DEMO 3: Join Queries")
    runner.demo_joins()

    # ============================================================
    # PART 2 — FINAL DATA EXTRACTION
    # ============================================================

    logger.info("\n[EXTRACT] Starting production extraction...")

    extractor = DataExtractor()

    extractor.extract().save().report()


if __name__ == "__main__":
    main()