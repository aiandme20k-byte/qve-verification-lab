# QVE Verification Lab — Prototype 1
Scientific evidence ledger + deterministic analysis + 3D digital twin.

> This prototype does not establish physical propulsion or vacuum-energy extraction from correlation, visualization, simulation, or source-reported claims.

## Run
Backend:
```bash
cd backend
python -m venv .venv
# activate the environment
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Frontend:
```bash
cd frontend
npm install
npm run dev
```
Open the Vite URL shown in the terminal.

## Docker
`docker compose up --build`

## Evidence states
`ACTUAL_DATA`, `CALCULATED`, `SIMULATED`, `SOURCE_REPORTED`, `INCONCLUSIVE`, plus workflow states `DATA_SUPPORTED`, `REPLICATED`, `VERIFIED`.

Imported datasets are never automatically considered independently verified actual measurements.
