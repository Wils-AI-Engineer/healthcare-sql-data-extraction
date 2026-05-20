# ================================================================
# src/data_extractor.py
# ================================================================
# Purpose:
#   Run the final healthcare extraction query and save raw-data.csv.
#
# Pipeline:
#   SQL files → SQLQueryRunner → DataExtractor → data/raw-data.csv
# ================================================================

import sys, pathlib

# Find project root so config.py can be imported
_root = pathlib.Path(__file__).resolve().parent
while not (_root / "config.py").exists() and _root != _root.parent:
    _root = _root.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import pandas as pd
from config import INDUSTRY, RAW_DATA_PATH, DB_AVAILABLE, logger
from src.querry_runner import SQLQueryRunner

class DataExtractor:
    """
    Runs the production healthcare extraction query and saves raw-data.csv.

    SQLQueryRunner handles:
    - loading SQL files
    - running SQL against PostgreSQL
    - returning pandas DataFrames

    DataExtractor handles:
    - choosing the final extraction query
    - saving the output CSV
    - reporting extraction results
    """
    def __init__(self):
        self.industry = INDUSTRY    
        self.runner = SQLQueryRunner()
        self.raw_df = None
        self._status = "ready"

    def extract(self) -> "DataExtractor":
        """
        Runs the final extraction SQL query and stores results in self.raw_df.
        """

        logger.info("[EXTRACT] Starting healthcare data extraction")

        if DB_AVAILABLE:
            self.raw_df = self.runner.run_file("extract_raw_data.sql")
        else:
            logger.error("[EXTRACT] Database unavailable. Cannot extract data.")
            self.raw_df = pd.DataFrame()

        if self.raw_df is None or self.raw_df.empty:
            logger.warning("[EXTRACT] Query returned 0 rows.")
            self.raw_df = pd.DataFrame()

        self._status = "Extracted"

        logger.info(
            f"[EXTRACT] {len(self.raw_df):,} rows × "
            f"{self.raw_df.shape[1] if not self.raw_df.empty else 0} columns extracted"
        )

        return self
    
    def save(self) -> "DataExtractor":
        """
        Saves the extracted data to data/raw-data.csv.
        """
        if self.raw_df is None or self.raw_df.empty:
            logger.error("[EXTRACT] No data to save. Run extract() first.")
            return self

        self.raw_df.to_csv(RAW_DATA_PATH, index=False, encoding="utf-8")

        file_size_kb = RAW_DATA_PATH.stat().st_size / 1024

        logger.info(
            f"[EXTRACT] Saved {len(self.raw_df):,} rows to "
            f"{RAW_DATA_PATH.name} ({file_size_kb:.1f} KB)"
        )

        self._status = "Data Saved"

        return self
    
    def report(self) -> None:
        """
        Prints a summary of the extraction results.
        """

        if self.raw_df is None or self.raw_df.empty:
            print("No data extracted. Run extract() first.")
            return

        print()
        print("=" * 60)
        print("  HEALTHCARE SQL PROJECT — EXTRACTION COMPLETE")
        print("=" * 60)
        print(f"  Rows extracted:    {len(self.raw_df):,}")
        print(f"  Columns:           {self.raw_df.shape[1]}")
        print(f"  Output file:       {RAW_DATA_PATH}")
        print(
            f"  File size:         {RAW_DATA_PATH.stat().st_size / 1024:.1f} KB"
            if RAW_DATA_PATH.exists()
            else ""
        )

        print()
        print("  Null values in raw data:")
        nulls = self.raw_df.isna().sum()

        if nulls.sum() == 0:
            print("    No null values found.")
        else:
            for col in nulls[nulls > 0].index:
                pct = round(nulls[col] / len(self.raw_df) * 100, 1)
                print(f"    NULL {col}: {nulls[col]:,} rows ({pct}%)")

        print()
        print("  Deliverable created:")
        print("    data/raw-data.csv")
        print("=" * 60)

    def __str__(self):
        return f"DataExtractor(industry={self.industry!r}, status={self._status!r})"

    def __repr__(self):
        return f"DataExtractor(industry={self.industry!r})"
    