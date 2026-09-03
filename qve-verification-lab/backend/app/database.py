from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from app.config import settings
import json

# Create engine and session
engine = create_engine(
    settings.DATABASE_URL.replace("sqlite://", "sqlite:///"),
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database Models
class Dataset(Base):
    """Raw imported dataset with provenance."""
    __tablename__ = "datasets"
    
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True)
    import_type = Column(String)  # CSV, JSON
    sha256 = Column(String, index=True, unique=True)
    state = Column(String, default="SOURCE_REPORTED")  # ACTUAL_DATA, SOURCE_REPORTED, IMPORTED
    row_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)


class DataPoint(Base):
    """Individual data points from datasets."""
    __tablename__ = "data_points"
    
    id = Column(String, primary_key=True, index=True)
    dataset_id = Column(String, index=True)
    timestamp = Column(Float, index=True)
    value = Column(Float)
    field_name = Column(String, index=True)
    raw_value = Column(String)
    is_missing = Column(Boolean, default=False)
    is_outlier = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class QCResult(Base):
    """Quality control results."""
    __tablename__ = "qc_results"
    
    id = Column(String, primary_key=True, index=True)
    dataset_id = Column(String, index=True)
    check_type = Column(String)  # missing_values, duplicate_timestamps, sampling, outliers
    status = Column(String)  # PASS, FAIL, WARNING
    count = Column(Integer)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class Correlation(Base):
    """Calculated correlations between variables."""
    __tablename__ = "correlations"
    
    id = Column(String, primary_key=True, index=True)
    dataset_id = Column(String, index=True)
    var1 = Column(String)
    var2 = Column(String)
    pearson_r = Column(Float)
    p_value = Column(Float)
    interpretation = Column(String)  # MARKED AS NOT CAUSATION
    created_at = Column(DateTime, default=datetime.utcnow)


class EnergyCalculation(Base):
    """Energy accounting calculations."""
    __tablename__ = "energy_calculations"
    
    id = Column(String, primary_key=True, index=True)
    dataset_id = Column(String, index=True)
    calculation_type = Column(String)  # casimir, radiation_momentum
    value = Column(Float)
    unit = Column(String)
    method = Column(String)
    uncertainty = Column(Float)
    state = Column(String, default="CALCULATED")
    created_at = Column(DateTime, default=datetime.utcnow)


class Claim(Base):
    """Evidence claims with state machine."""
    __tablename__ = "claims"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    state = Column(String, default="DRAFT")  # DRAFT, UNDER_REVIEW, GATE_A, GATE_B, GATE_C, GATE_D, GATE_E, GATE_F, VERIFIED, REJECTED
    supporting_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class EvidenceGate(Base):
    """Evidence gate evaluation results."""
    __tablename__ = "evidence_gates"
    
    id = Column(String, primary_key=True, index=True)
    claim_id = Column(String, index=True)
    gate_name = Column(String)  # A, B, C, D, E, F
    status = Column(String)  # PASS, FAIL, INCONCLUSIVE
    evidence_details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    """Immutable audit trail."""
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, index=True)
    action = Column(String)
    actor = Column(String)
    resource_type = Column(String)
    resource_id = Column(String)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class TelemetryReplay(Base):
    """Stored telemetry for replay visualization."""
    __tablename__ = "telemetry_replays"
    
    id = Column(String, primary_key=True, index=True)
    dataset_id = Column(String, index=True)
    frame_index = Column(Integer)
    position_x = Column(Float)
    position_y = Column(Float)
    position_z = Column(Float)
    velocity_x = Column(Float)
    velocity_y = Column(Float)
    velocity_z = Column(Float)
    energy = Column(Float)
    timestamp = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db() -> Session:
    """Get database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create all tables
Base.metadata.create_all(bind=engine)
