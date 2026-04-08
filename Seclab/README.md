## Lab 2 - Server Application

This repository implements a three-layer server-side application as required by the lab assignment.

1. **Data Access Layer** – defines interfaces and an SQLAlchemy-based implementation that reads from a CSV file and persists models to a SQLite database.
2. **Business Logic Layer** – contains logic that consumes the data-access interface, transforms rows into domain models, and instructs the data layer to save them.
3. **Presentation Layer** – currently represented only by interfaces; no UI or logic is implemented yet.

All data originates from a single CSV file (generated via the `generate_data` module) with at least 1 000 lines. The business logic processes this file and populates the `tickets.db` SQLite database.

## Swagger API

A Swagger-enabled Flask API is available at `Seclab/app/api.py`.

To run:

1. install dependencies:
   - `pip install -r requirements.txt`
2. run the API:
   - `python -m app.api`
3. open Swagger UI:
   - `http://localhost:5001/apidocs/`

Endpoints:
- `POST /login` - login with JSON `{ "username": "admin", "password": "password" }` to get JWT token
- `GET /tickets` - list all tickets (requires JWT)
- `POST /tickets/process` - process CSV by JSON payload `{ "csv_path": "data.csv" }` (requires JWT)
- `POST /tickets/upload` - upload CSV file (requires JWT)

## Run with Docker Compose

From the repository root:

```bash
docker compose up --build
```

This will start:

- `seclab` API on `http://localhost:5001`
- `redis` on `localhost:6379`
- `kafka` on `localhost:9092`
- `zookeeper` on `localhost:2181`

The Flask API is configured to bind to `0.0.0.0` inside the container so the port mapping works correctly.
