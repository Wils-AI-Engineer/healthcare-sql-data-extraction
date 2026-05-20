# ================================================================
# src/query_runner.py
# ================================================================
# Purpose:
#   Run SQL queries from Python and return results as pandas DataFrames.
#   This is to etract a final CSV file ready for ETL analysis.
# ================================================================

import sys
import pathlib
import time
import pandas as pd

# Find project root so config.py can be imported
_root = pathlib.Path(__file__).resolve().parent
while not (_root / "config.py").exists() and _root != _root.parent:
    _root = _root.parent

if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from config import engine, DB_AVAILABLE, SQL_DIR, INDUSTRY, logger

class SQLQueryRunner:
    """
    Executes SQL queries against the Supabase PostgreSQL database.
    Returns results as pandas DataFrames.
    """

    def __init__(self):
        self.industry = INDUSTRY
        self.history = []
        logger.info(f"SQLQueryRunner ready — db_available: {DB_AVAILABLE}")

    def run(self, sql: str, params: dict = None) -> pd.DataFrame:
        """
        Execute a SQL query and return the result as a DataFrame.
        """

        if not DB_AVAILABLE or engine is None:
            logger.warning("[SQL] Database not available. Returning empty DataFrame.")
            return pd.DataFrame()

        # Replace placeholders if used in SQL files
        sql = sql.replace("{industry}", self.industry)

        start_time = time.time()

        try:
            df = pd.read_sql(sql, engine, params=params)

            duration_ms = round((time.time() - start_time) * 1000, 1)

            self.history.append({
                "sql_preview": sql[:80].strip(),
                "rows": len(df),
                "cols": len(df.columns),
                "duration_ms": duration_ms,
                "status": "success",
            })

            logger.info(
                f"[SQL] Query complete — "
                f"{len(df):,} rows × {len(df.columns)} cols | "
                f"{duration_ms}ms"
            )

            return df

        except Exception as e:
            duration_ms = round((time.time() - start_time) * 1000, 1)

            self.history.append({
                "sql_preview": sql[:80].strip(),
                "rows": 0,
                "cols": 0,
                "duration_ms": duration_ms,
                "status": f"error: {str(e)[:100]}",
            })

            logger.error(f"[SQL] Query failed: {e}")
            return pd.DataFrame()
        
    def run_file(self, filename: str) -> pd.DataFrame:
        """
        Load and run a SQL file from the sql/ folder.
        """
        sql_path = SQL_DIR / filename

        if not sql_path.exists():
            logger.error(f"[SQL] File not found: {sql_path}")
            return pd.DataFrame()

        logger.info(f"[SQL] Loading file: {filename}")

        sql_text = sql_path.read_text(encoding="utf-8")

        return self.run(sql_text)

    def demo_basics(self) -> None:
        """
        Run a basic healthcare query.
        """
        sql = f"""
            SELECT *
            FROM {self.industry}.patients
            LIMIT 10;
        """
        print("\n── Sample Patients Data:")
        df = self.run(sql)

        if not df.empty:
            print(df.to_string(index=False))

    def demo_aggregation(self) -> None:
        """
        Run an aggregation query on appointments.
        """
        sql = f"""
            SELECT
                status AS appointment_status,
                COUNT(*) AS appointment_count
            FROM {self.industry}.appointments
            GROUP BY status
            ORDER BY appointment_count DESC;
        """
        print("\n── Appointment Count by Status:")
        df = self.run(sql)

        if not df.empty:
            print(df.to_string(index=False))

    def demo_joins(self) -> None:
        """
        Run a joined healthcare query.
        """
        sql = f"""
            SELECT
                p.patient_id,
                p.first_name AS patient_first_name,
                p.last_name AS patient_last_name,
                a.appointment_id,
                a.appointment_date,
                a.status AS appointment_status,
                b.bill_id,
                b.amount_charged,
                b.payment_status
            FROM {self.industry}.patients AS p
            JOIN {self.industry}.appointments AS a
                ON p.patient_id = a.patient_id
            LEFT JOIN {self.industry}.billing AS b
                ON a.appointment_id = b.appointment_id
            LIMIT 10;
        """

        print("\n── Patient Appointment Billing Join:")
        df = self.run(sql)

        if not df.empty:
            print(df.to_string(index=False))

    def __str__(self) -> str:
        return f"SQLQueryRunner(Industry={self.industry!r}, queries_run={len(self.history)})"

    def __repr__(self) -> str:
        return f"SQLQueryRunner(Industry={self.industry!r})"
