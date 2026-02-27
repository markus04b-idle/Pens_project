# Pens_project

This repository holds a simple dataset for a hockey team (the "Pens") extracted
from HTML snippets.  The files include:

* `roster.csv` – player roster with forwards, defensemen, and goalies.
* `stats.csv` – season statistics for skaters and goalies.
* `models.py` – SQLModel classes defining the schema.
* `create_db.py` – script to build `penguins.db` and populate it from the CSVs.

## Building the database

To recreate the SQLite database run:

```bash
python3 create_db.py
```

That will remove any existing `penguins.db`, create the tables defined in
`models.py`, and load the CSV files into the appropriate tables.  You can then
inspect the database using `sqlite3` or a GUI tool.
