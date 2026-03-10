## Lab 2 - Server Application

This repository implements a three-layer server-side application as required by the lab assignment.

1. **Data Access Layer** – defines interfaces and an SQLAlchemy-based implementation that reads from a CSV file and persists models to a SQLite database.
2. **Business Logic Layer** – contains logic that consumes the data-access interface, transforms rows into domain models, and instructs the data layer to save them.
3. **Presentation Layer** – currently represented only by interfaces; no UI or logic is implemented yet.

All data originates from a single CSV file (generated via the `generate_data` module) with at least 1 000 lines. The business logic processes this file and populates the `tickets.db` SQLite database.