# Healthcare SQL Project

## Project Overview

--- 
This project simulates a real-world healthcare analytics workflow using PostgreSQL, SQL, Python, and pandas.

The objective is to extract operational healthcare data from a PostgreSQL database hosted on Supabase and generate a raw dataset for downstream ETL processing.

The final deliverable is:

```bash
data/raw-data.csv
```

This dataset combines:
- patient records
- appointment history
- billing information
- doctor information
- department data

The extracted CSV is designed to serve as the raw input for a future ETL pipeline:
---

## Business Scenario

### Company:

**MedCore Analytics**

### Client:
**St. Aurelius General Hospital**

### Role:
**Data Analyst**

The finance and analytics teams require a unified extract combining healthcare operational data from multiple PostgreSQL tables.

The solution involves:
- querying the `healthcare` schema
- joining multiple related tables
- performing aggregation and advanced SQL analysis
- exporting the results to CSV using Python

---

## Technologies Used

- Python 3
- PostgreSQL
- Supabase
- SQLAlchemy
- pandas
- psycopg2
- python-dotenv
- DBeaver
- Git & GitHub

---

## Project Structure

```bash
Healthcare-sql-project/
│
├── data/
│   ├── .gitkeep
│   └── raw-data.csv
│
├── sql/
│   ├── basics.sql
│   ├── aggregation.sql
│   ├── joins.sql
│   ├── extract_raw_data.sql
│   └── advanced.sql
│
├── src/
│   ├── querry_runner.py
│   └── data_extractor.py
│
├── tests/
│   └── test_sql.py
│
├── .env
├── .gitignore
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

---

## Database Schema

Schema used:

```sql
healthcare
```

Main tables:
- `patients`
- `appointments`
- `billing`
- `doctors`
- `departments`

---

## SQL Concepts Implemented

## 1. Basic SQL Queries
- `SELECT`
- `WHERE`
- `ORDER BY`
- `LIMIT`

## 2. Aggregation
- `COUNT()`
- `SUM()`
- `AVG()`
- `GROUP BY`

## 3. Joins
- `JOIN`
- `LEFT JOIN`

## 4. Advanced SQL
- Common Table Expressions (CTEs)
- Window Functions
- `RANK() OVER()`

---

## Final Extraction Query

The final extraction query:
- joins patients, appointments, billing, doctors, and departments
- creates a flat analytics-ready dataset
- exports the data to CSV

Output file:

```bash
data/raw-data.csv
```

---

## Setup Instructions

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Healthcare-sql-project
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv healthcare-env
healthcare-env\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv healthcare-env
source healthcare-env/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
DB_URL=postgresql+psycopg2://USER:PASSWORD@HOST:5432/postgres
```

---

## Running the Project

Run the complete workflow:

```bash
python run.py
```

This will:
1. Demonstrate SQL queries
2. Execute the final extraction query
3. Generate `raw-data.csv`
4. Print extraction reports

---

## Running Unit Tests

Run tests with:

```bash
python tests/test_sql.py
```

The tests verify:
- SQL file existence
- SQL query structure
- JOIN logic
- CTE/window functions
- query execution
- CSV extraction workflow

---

## Example Output

Generated file:

```bash
data/raw-data.csv
```

Contains:
- patient demographics
- appointment details
- billing data
- doctor information
- department information
- metadata columns

---


## Data Quality Considerations

The extracted raw data may intentionally contain:
- NULL values
- incomplete billing records
- inconsistent operational records

These issues are expected and would normally be handled during the ETL and data cleaning phases.

---

## Future Improvements

Possible enhancements:
- add automated ETL pipeline
- build analytics dashboards
- implement database migrations
- add Docker support
- add CI/CD testing
- schedule automated extractions

---

## Author

Wilson Sunday Echara

---

## License

This project is for educational and portfolio purposes.