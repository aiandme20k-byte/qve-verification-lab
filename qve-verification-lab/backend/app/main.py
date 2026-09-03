from fastapi import FastAPI, UploadFile, File, HTTPException
from .services.hashing import sha256_bytes
from .services.qc import qc_dataframe
from .services.physics import casimir_force, radiation_force, energy_balance
from .services.statistics import correlation
import pandas as pd, io, json, uuid

app=FastAPI(title="QVE Verification Lab API", version="0.1.0")

@app.get("/health")
def health(): return {"status":"ok","project":"QVE Verification Lab","release":"Prototype 1"}

@app.post("/datasets/import")
async def import_dataset(file: UploadFile=File(...)):
    raw=await file.read()
    digest=sha256_bytes(raw)
    try:
        if file.filename.lower().endswith(".json"):
            obj=json.loads(raw.decode())
            df=pd.DataFrame(obj if isinstance(obj,list) else obj.get("rows",[]))
        else: df=pd.read_csv(io.BytesIO(raw))
    except Exception as e: raise HTTPException(400,f"Cannot parse dataset: {e}")
    return {"datasetId":"DS-"+uuid.uuid4().hex[:8].upper(),"filename":file.filename,"sha256":digest,
            "sampleCount":len(df),"columns":list(df.columns),"dataStatus":"IMPORTED"}

@app.post("/qc/run")
async def run_qc(file: UploadFile=File(...)):
    raw=await file.read()
    df=pd.read_csv(io.BytesIO(raw))
    return qc_dataframe(df)

@app.post("/analysis/correlation")
async def corr(payload: dict):
    return correlation(payload["x"],payload["y"])

@app.post("/analysis/force")
def force(payload: dict):
    return casimir_force(payload["area_m2"],payload["separation_m"])

@app.post("/analysis/radiation-force")
def rad(payload: dict):
    return radiation_force(payload["power_w"])

@app.post("/analysis/energy")
def energy(payload: dict):
    return energy_balance(payload["output_w"],payload["input_w"],payload.get("loss_w",0.0))
