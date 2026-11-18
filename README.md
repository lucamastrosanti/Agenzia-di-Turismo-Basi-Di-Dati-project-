# Italy Tourism Web Application

A small university project developed in May 2026 for the **Database (Basi di Dati)** course at Politecnico di Torino.

The application is an interactive Streamlit dashboard for exploring a local MySQL tourism/hotel database. It provides an overview of partner travel agencies, room search and filtering, and economic analysis of bookings.

## Features

### Agencies

- Displays the total number of agencies and cities.
- Identifies the city with the highest number of agencies.
- Filters agencies by city.
- Builds complete addresses with SQL `CONCAT`.
- Shows filtered agency locations on a geographical map.
- Lists agency codes, phone numbers, and addresses.

### Rooms

- Filters rooms by type: single, double, triple, or all.
- Loads available optional services dynamically from the database.
- Supports filtering by multiple optional services.
- Can restrict results to rooms that include a kitchen.
- Displays matching rooms in a table.
- Shows a preview of up to five matching rooms with example images.

### Reservations

- Calculates the length of each stay and a daily room cost.
- Finds the room with the highest average daily cost in each month.
- Displays the monthly average daily cost in a table and line chart.

## Technology

- Python
- Streamlit
- Pandas
- NumPy
- MySQL
- mysql-connector-python
- SQLAlchemy

## Application Structure

```text
.
├── Home.py                 # Main Streamlit page
├── pages/
│   ├── 1_Agenzie.py        # Agency metrics, search, and map
│   ├── 2_Stanze.py         # Room filtering and previews
│   └── 3_Prenotazioni.py   # Reservation analysis and charts
├── images/
│   └── polito_white.png
├── requirements.txt
├── Pipfile
├── readme_windows.md
└── LICENSE
```

## Database Requirements

The application connects to a local MySQL server and expects a database named `hotel`:

```text
host: localhost
user: root
password: empty by default
database: hotel
```

The code assumes that the database contains at least the following tables and columns:

| Table | Main columns used |
|---|---|
| `AGENZIA` | `CodA`, `Tel`, `Via_Indirizzo`, `Numero_Indirizzo`, `Citta_Indirizzo` |
| `CITTA` | `Nome`, `Latitudine`, `Longitudine` |
| `STANZA` | `CodS`, `Piano`, `Superficie`, `Type` |
| `HAS_OPTIONAL` | `STANZA_CodS`, `OPTIONAL_Optional` |
| `HAS_SPAZI` | `STANZA_CodS`, `SPAZI_Spazi` |
| `PRENOTAZIONE` | `STANZA_CodS`, `DataInizio`, `DataFine`, `Costo` |

The database dump or schema creation script is not included in this repository. The MySQL `hotel` database must therefore be created and populated separately before starting the application.

## Installation

Python 3.9 is recommended to match the Pipfile. A virtual environment is also recommended.

### 1. Clone the repository

```bash
git clone https://github.com/lucamastrosanti/Agenzia-di-Turismo-Basi-Di-Dati-project-.git
cd Agenzia-di-Turismo-Basi-Di-Dati-project-
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Or on Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
python -m pip install mysql-connector-python
```

The `mysql-connector-python` package is used directly by the application but is not listed in `requirements.txt`.

### 4. Configure MySQL

Start MySQL on `localhost` and make sure the `hotel` database uses the schema expected by the application.

If MySQL credentials differ from `root` with an empty password, update the `get_connection()` function in each page:

```python
mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hotel"
)
```

For a Docker-based MySQL setup, start a MySQL container and configure its host, port, username, password, and database accordingly.

### 5. Run the application

From the repository root:

```bash
python -m streamlit run Home.py
```

Streamlit will print the local URL, normally `http://localhost:8501`.

## Notes

- Room and agency previews depend on the data available in the local `hotel` database.
- Room images are loaded from external Unsplash URLs.
- The reservation analysis uses `DataInizio` to assign a booking to a month.
- A stay with a start and end date that are equal or reversed is normalized to one day to avoid division by zero.
- All database connection settings are currently stored directly in the Python page files.

## Author

**Luca Mastrosanti**  
Computer Engineering — Politecnico di Torino

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.
