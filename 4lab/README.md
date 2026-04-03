# Lab 4 — Variant 26

This Lab 4 solution fetches data from the NYC Open Data Parking Violations API and saves it locally.

## Assignment

Variant 26 uses the NYC Parking Violations Issued Fiscal Year 2019 dataset from the following API:

- https://data.cityofnewyork.us/resource/pvqr-7yc4.json

The application downloads records from the API, writes them to a file, and can print a summary report.

## How to run

From the `4lab` folder:

```bash
python -m app.main --limit 1000 --output parking_violations_2019.json --format json --summary
```

Or save CSV instead:

```bash
python -m app.main --limit 1000 --output parking_violations_2019.csv --format csv --summary
```

## Docker Compose for Lab 4

A dedicated compose file is available at `4lab/docker-compose.yml`.

To run Lab 4 with Docker Compose:

```bash
cd 4lab
docker compose up --build
```

This will start the Lab 4 container and execute the fetch command using the local app code.

It also starts supporting services:

- `redis` on `localhost:6379`
- `zookeeper` on `localhost:2181`
- `kafka` on `localhost:9092`

The output destination is selected using the strategy configuration in `config.json` or with environment variables.

To switch output behavior, use either `config.ini` or `config.json`.

In `config.ini`, set `output_strategy` under `[output]`:

```ini
[output]
strategy = file
file_path = output_records.json
```

Available strategies:
- `console`
- `file`
- `redis`
- `kafka`

Or override the strategy with an environment variable in `docker-compose.yml`:

```yaml
environment:
  OUTPUT_STRATEGY: redis
```

When `file` is selected, the output file path is taken from `file_path` or `OUTPUT_FILE_PATH`.
When Redis is selected, records are written to the key from `REDIS_KEY`.
When Kafka is selected, records are published to the topic from `KAFKA_TOPIC`.

## Notes

- `--limit` controls how many records are downloaded.
- `--format` can be `json` or `csv`.
- `--summary` prints the top violation codes, street names, and vehicle makes.
