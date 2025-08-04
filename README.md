# Hawaii Climate Analysis & Flask API

> Exploratory climate analysis on Honolulu-area weather data plus a lightweight REST API that serves precipitation and temperature stats from a local SQLite database.

## Summary
This project has two parts:
1) a **pandas/SQLAlchemy** workflow that explores precipitation and temperature observations from multiple weather stations in Hawaii, and  
2) a **Flask API** backed by `hawaii.sqlite` that exposes clean endpoints for downstream apps or dashboards.  
It delivers refreshable tables/plots (last-12-months precipitation, active stations, temperature distributions) and programmatic access to daily measurements and date-range aggregates.

## Goal
- **Primary:** Make Hawaii climate data **analysis-ready** and **accessible via API** for quick insight and reuse.
- **Secondary:** Provide reproducible queries (by date range, by station) to support planning (tourism, events), research, and demos.

## Procedure
1. **Data Ingestion**
   - Load `hawaii_measurements.csv` and `hawaii_stations.csv`.
   - Create/refresh `hawaii.sqlite`; reflect tables with SQLAlchemy.
2. **Exploratory Analysis (notebook)**
   - Compute **last 12 months** of precipitation by date.
   - Identify **most active station(s)**; summarize temperature observations (min/avg/max).
   - Plot distributions and time series for precipitation and temperature.
3. **API Development (Flask)**
   - Build read-only endpoints that query SQLite via SQLAlchemy sessions.
   - Serialize responses to JSON with clear keys and ISO dates.
4. **Validation**
   - Spot-check row counts, date ranges, and station IDs.
   - Basic schema/NA checks and sanity comparisons with notebook outputs.

## Result
- **Implemented Endpoints**
  - `/api/v1.0/precipitation` → `{ "2017-08-23": 0.00, "2017-08-22": 0.50, ... }`
  - `/api/v1.0/stations` → `["USC00519397", "USC00519281", ...]`
  - `/api/v1.0/tobs` → last-12-months temperature observations for the most active station.
  - `/api/v1.0/<start>` → temperature **TMIN/TAVG/TMAX** from `<start>` to latest.
  - `/api/v1.0/<start>/<end>` → temperature **TMIN/TAVG/TMAX** for the date range.
- **Analysis Artifacts**
  - Tables/figures for: precipitation over time, station activity ranking, and temperature summaries.

## Business Impact
- **Decision support:** Quick checks on expected rainfall/temperature improve **event planning** and **tourism ops**.
- **Reuse & integration:** A stable API enables **dashboards**, **notebooks**, or **prototype apps** to consume the same vetted data.
- **Education & demos:** Compact, end-to-end example of data → analysis → service for teaching analytics engineering.

## Next Step to Make It Better
- **Data & Quality**
  - Add more years/stations and metadata (elevation, microclimate); build unit tests (e.g., Great Expectations).
- **Performance & Ops**
  - Add caching (per-route), pagination for long date ranges, and DB indexes on date/station.
  - Containerize (Docker) and add CI/CD with basic health checks.
- **Product & DX**
  - Provide OpenAPI/Swagger docs, query params (e.g., `?station=...`), and error handling with clear messages.
  - Ship a small Streamlit/Plotly UI that calls the API for interactive charts.
- **Analytics**
  - Seasonal/rolling stats, anomaly flags, simple forecasts (Prophet/ARIMA), and rainfall percentile lookups.

---

### (Optional) How to Run

```bash
# 1) Environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # or: pip install flask sqlalchemy pandas matplotlib

# 2) Initialize DB (if starting from CSVs)
# Run the notebook or a small setup script to (re)create hawaii.sqlite

# 3) Start API
export FLASK_APP=app.py
flask run  # or: python app.py

# 4) Test
curl http://127.0.0.1:5000/api/v1.0/precipitation
````

### (Optional) Tech Stack

**Python:** pandas, SQLAlchemy, Flask
**Storage:** SQLite (`hawaii.sqlite`)
**Viz (notebook):** Matplotlib/Plotly (optional)
