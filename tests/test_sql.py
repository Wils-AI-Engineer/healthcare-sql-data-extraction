# ================================================================
# tests/test_sql.py — Unit Tests for Healthcare SQL Project
# ================================================================

import sys, pathlib
_root = pathlib.Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import pandas as pd
from src.querry_runner   import SQLQueryRunner
from src.data_extractor import DataExtractor

def test_sql_files_exist():
    """Required SQL files must exist in the sql/ directory."""
    from config import SQL_DIR

    expected = [
        "basics.sql",
        "aggregation.sql",
        "joins.sql",
        "extract_raw_data.sql",
        "advanced.sql",
    ]

    for fname in expected:
        assert (SQL_DIR / fname).exists(), f"SQL file missing: {fname}"

    print("  PASS: test_sql_files_exist")

def test_sql_files_contain_select_keyword():
    """Each SQL file must contain at least one SELECT statement."""
    from config import SQL_DIR

    expected = [
        "basics.sql",
        "aggregation.sql",
        "joins.sql",
        "extract_raw_data.sql",
        "advanced.sql",
    ]

    for fname in expected:
        content = (SQL_DIR / fname).read_text(encoding="utf-8")
        assert "SELECT" in content.upper(), f"No SELECT found in {fname}"

    print("  PASS: test_sql_files_contain_select_keyword")


def test_final_extract_contains_required_tables():
    """Final extract SQL must join patients, appointments, and billing."""
    from config import SQL_DIR

    content = (SQL_DIR / "extract_raw_data.sql").read_text(encoding="utf-8").lower()

    required_tables = [
        "healthcare.patients",
        "healthcare.appointments",
        "healthcare.billing",
    ]

    for table in required_tables:
        assert table in content, f"Missing required table in final extract: {table}"

    print("  PASS: test_final_extract_contains_required_tables")

def test_final_extract_contains_join():
    """Final extract SQL must use JOIN logic."""
    from config import SQL_DIR

    content = (SQL_DIR / "extract_raw_data.sql").read_text(encoding="utf-8").upper()

    assert "JOIN" in content, "Final extract must contain at least one JOIN"

    print("  PASS: test_final_extract_contains_join")


def test_cte_or_window_file_contains_advanced_sql():
    """Advanced SQL file must contain a CTE or window function."""
    from config import SQL_DIR

    content = (SQL_DIR / "advanced.sql").read_text(encoding="utf-8").upper()

    has_cte = "WITH" in content
    has_window = "OVER" in content

    assert has_cte or has_window, "advanced.sql must contain a CTE or window function"

    print("  PASS: test_cte_or_window_file_contains_advanced_sql")


def test_query_runner_returns_dataframe():
    """SQLQueryRunner.run() must return a DataFrame."""
    runner = SQLQueryRunner()

    df = runner.run("SELECT 1 AS test_col")

    assert isinstance(df, pd.DataFrame), "run() must return a DataFrame"

    print("  PASS: test_query_runner_returns_dataframe")


def test_query_runner_handles_bad_sql_gracefully():
    """Bad SQL should return an empty DataFrame instead of crashing."""
    runner = SQLQueryRunner()

    df = runner.run("THIS IS NOT VALID SQL")

    assert isinstance(df, pd.DataFrame), "run() should return a DataFrame even on error"
    assert df.empty, "Bad SQL should return an empty DataFrame"

    print("  PASS: test_query_runner_handles_bad_sql_gracefully")


def test_query_runner_history_records_each_run():
    """Every query run should be recorded in history."""
    runner = SQLQueryRunner()

    initial_count = len(runner.history)

    runner.run("SELECT 1 AS one")
    runner.run("SELECT 2 AS two")

    assert len(runner.history) == initial_count + 2, "history should record each query run"

    print("  PASS: test_query_runner_history_records_each_run")


def test_data_extractor_initializes():
    """DataExtractor should initialise correctly."""
    extractor = DataExtractor()

    assert extractor.runner is not None, "DataExtractor should have an SQLQueryRunner"
    assert extractor.raw_df is None, "raw_df should start as None"

    print("  PASS: test_data_extractor_initializes")


def test_data_extractor_extract_returns_self():
    """extract() should return self so chaining works."""
    extractor = DataExtractor()

    result = extractor.extract()

    assert result is extractor, "extract() should return self"
    assert isinstance(extractor.raw_df, pd.DataFrame), "raw_df should be a DataFrame after extract()"

    print("  PASS: test_data_extractor_extract_returns_self")


if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  HEALTHCARE SQL PROJECT — UNIT TESTS")
    print("=" * 60)
    print()

    test_sql_files_exist()
    test_sql_files_contain_select_keyword()
    test_final_extract_contains_required_tables()
    test_final_extract_contains_join()
    test_cte_or_window_file_contains_advanced_sql()
    test_query_runner_returns_dataframe()
    test_query_runner_handles_bad_sql_gracefully()
    test_query_runner_history_records_each_run()
    test_data_extractor_initializes()
    test_data_extractor_extract_returns_self()

    print()
    print("=" * 60)
    print("  All tests passed ✓")
    print("=" * 60)