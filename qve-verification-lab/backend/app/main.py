"""QVE Verification Lab FastAPI Application."""
from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uuid
import os
from datetime import datetime

from app.database import get_db, engine, Base, Dataset, DataPoint, QCResult, Claim, EvidenceGate, AuditLog
from app.config import settings
from app import schemas, analysis, evidence

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="QVE Verification Lab — Prototype 1",
    description="Scientific evidence ledger + deterministic analysis + 3D digital twin",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


# Dataset endpoints
@app.post("/api/datasets/import", response_model=schemas.DatasetResponse)
async def import_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import CSV or JSON dataset.
    
    WARNING: Imported datasets are marked as SOURCE_REPORTED.
    They are never automatically considered independently verified actual measurements.
    """
    try:
        # Save uploaded file
        os.makedirs(settings.DATA_DIR, exist_ok=True)
        file_path = os.path.join(settings.DATA_DIR, file.filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Determine import type and process
        if file.filename.endswith('.csv'):
            records, sha256, row_count = analysis.import_csv(file_path)
            import_type = "CSV"
        elif file.filename.endswith('.json'):
            records, sha256, row_count = analysis.import_json(file_path)
            import_type = "JSON"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use CSV or JSON.")
        
        # Create dataset record
        dataset_id = str(uuid.uuid4())
        dataset = Dataset(
            id=dataset_id,
            filename=file.filename,
            import_type=import_type,
            sha256=sha256,
            state="SOURCE_REPORTED",  # STRICT: Imported data is SOURCE_REPORTED
            row_count=row_count,
            metadata={"original_filename": file.filename}
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        
        # Store individual data points
        for idx, record in enumerate(records):
            dp_id = str(uuid.uuid4())
            data_point = DataPoint(
                id=dp_id,
                dataset_id=dataset_id,
                timestamp=float(record.get("timestamp", idx)),
                value=float(record.get("value", 0)) if "value" in record else None,
                field_name=list(record.keys())[0] if record else "unknown",
                raw_value=str(record)
            )
            db.add(data_point)
        
        db.commit()
        
        # Audit log
        audit = AuditLog(
            id=str(uuid.uuid4()),
            action="DATASET_IMPORTED",
            actor="system",
            resource_type="Dataset",
            resource_id=dataset_id,
            details={"filename": file.filename, "sha256": sha256}
        )
        db.add(audit)
        db.commit()
        
        return schemas.DatasetResponse.from_attributes(**dataset.__dict__)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/datasets/{dataset_id}", response_model=schemas.DatasetResponse)
def get_dataset(dataset_id: str, db: Session = Depends(get_db)):
    """Retrieve dataset by ID."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return schemas.DatasetResponse.from_attributes(**dataset.__dict__)


# QC endpoints
@app.post("/api/qc/{dataset_id}")
def run_qc(dataset_id: str, db: Session = Depends(get_db)):
    """Run quality control checks on dataset."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Get data points
    data_points = db.query(DataPoint).filter(DataPoint.dataset_id == dataset_id).all()
    records = [{"value": dp.value, "timestamp": dp.timestamp} for dp in data_points]
    values = [dp.value for dp in data_points if dp.value is not None]
    
    qc_results = []
    
    # Missing values check
    missing_check = analysis.check_missing_values(records)
    qc_id = str(uuid.uuid4())
    qc_obj = QCResult(
        id=qc_id,
        dataset_id=dataset_id,
        check_type="missing_values",
        status=missing_check["status"],
        count=missing_check["missing_count"],
        details=missing_check
    )
    db.add(qc_obj)
    qc_results.append(missing_check)
    
    # Duplicate timestamps check
    dup_check = analysis.check_duplicate_timestamps(records)
    qc_id = str(uuid.uuid4())
    qc_obj = QCResult(
        id=qc_id,
        dataset_id=dataset_id,
        check_type="duplicate_timestamps",
        status=dup_check["status"],
        count=dup_check["duplicate_count"],
        details=dup_check
    )
    db.add(qc_obj)
    qc_results.append(dup_check)
    
    # Outliers check
    if values:
        outlier_check = analysis.check_outliers(values)
        qc_id = str(uuid.uuid4())
        qc_obj = QCResult(
            id=qc_id,
            dataset_id=dataset_id,
            check_type="outliers",
            status=outlier_check["status"],
            count=outlier_check["outlier_count"],
            details=outlier_check
        )
        db.add(qc_obj)
        qc_results.append(outlier_check)
    
    db.commit()
    
    return {"dataset_id": dataset_id, "qc_results": qc_results}


# Correlation endpoint
@app.post("/api/correlation/{dataset_id}")
def calculate_correlation(dataset_id: str, var1_field: str, var2_field: str, db: Session = Depends(get_db)):
    """Calculate Pearson correlation between two variables.
    
    STRICT: Correlation ≠ Causation
    This result is MARKED as NOT CAUSATION.
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # TODO: Extract var1 and var2 from data points
    var1 = []
    var2 = []
    
    r, p_value = analysis.calculate_pearson_correlation(var1, var2)
    
    correlation = {
        "id": str(uuid.uuid4()),
        "dataset_id": dataset_id,
        "var1": var1_field,
        "var2": var2_field,
        "pearson_r": r,
        "p_value": p_value,
        "interpretation": "NOT CAUSATION - Correlation does not establish causality"
    }
    
    return correlation


# Physics calculation endpoints
@app.post("/api/physics/casimir")
def calculate_casimir(area_m2: float, gap_nm: float):
    """Calculate ideal Casimir force.
    
    WARNING: This is CALCULATED theoretical force.
    SIMULATED data can never become ACTUAL_DATA.
    Internal Casimir forces do not automatically establish net spacecraft thrust.
    """
    force = analysis.calculate_casimir_force(area_m2, gap_nm)
    return {
        "force_newtons": force,
        "area_m2": area_m2,
        "gap_nm": gap_nm,
        "state": "CALCULATED",
        "note": "Theoretical calculation. Not experimental proof. Does not establish propulsion."
    }


@app.post("/api/physics/radiation")
def calculate_radiation(energy_joules: float):
    """Calculate radiation momentum.
    
    WARNING: This is theoretical momentum.
    NOT proof of spacecraft propulsion.
    """
    momentum = analysis.calculate_radiation_momentum(energy_joules)
    return {
        "momentum_kg_m_s": momentum,
        "energy_joules": energy_joules,
        "state": "CALCULATED",
        "note": "Theoretical calculation. Not experimental proof."
    }


# Evidence gate endpoints
@app.post("/api/evidence/gate/{gate_letter}")
def evaluate_gate(gate_letter: str, evidence_data: dict, db: Session = Depends(get_db)):
    """Evaluate evidence gate."""
    gate_framework = evidence.EvidenceGateFramework()
    
    if gate_letter.upper() == "A":
        result = gate_framework.gate_a_data_integrity(evidence_data)
    elif gate_letter.upper() == "B":
        result = gate_framework.gate_b_quality_control(evidence_data.get("qc_results", []))
    elif gate_letter.upper() == "C":
        result = gate_framework.gate_c_reproducibility(evidence_data)
    elif gate_letter.upper() == "D":
        result = gate_framework.gate_d_independence(evidence_data)
    elif gate_letter.upper() == "E":
        result = gate_framework.gate_e_theoretical_consistency(evidence_data)
    elif gate_letter.upper() == "F":
        result = gate_framework.gate_f_causality_and_propulsion(evidence_data)
    else:
        raise HTTPException(status_code=400, detail="Invalid gate letter. Use A-F.")
    
    return result


# Claim endpoints
@app.post("/api/claims", response_model=schemas.ClaimResponse)
def create_claim(claim: schemas.ClaimCreate, db: Session = Depends(get_db)):
    """Create a new evidence claim."""
    claim_id = str(uuid.uuid4())
    claim_obj = Claim(
        id=claim_id,
        title=claim.title,
        description=claim.description,
        state="DRAFT",
        supporting_data=claim.supporting_data or {}
    )
    db.add(claim_obj)
    db.commit()
    db.refresh(claim_obj)
    
    return schemas.ClaimResponse.from_attributes(**claim_obj.__dict__)


@app.get("/api/claims/{claim_id}", response_model=schemas.ClaimResponse)
def get_claim(claim_id: str, db: Session = Depends(get_db)):
    """Retrieve claim by ID."""
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return schemas.ClaimResponse.from_attributes(**claim.__dict__)


# Audit log endpoints
@app.get("/api/audit-logs")
def get_audit_logs(db: Session = Depends(get_db), limit: int = 100):
    """Retrieve audit logs."""
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()
    return [schemas.AuditLogResponse.from_attributes(**log.__dict__) for log in logs]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
