from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class DatasetCreate(BaseModel):
    filename: str
    import_type: str  # CSV, JSON


class DatasetResponse(BaseModel):
    id: str
    filename: str
    import_type: str
    sha256: str
    state: str
    row_count: int
    created_at: datetime
    metadata: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True


class QCResultResponse(BaseModel):
    id: str
    dataset_id: str
    check_type: str
    status: str
    count: int
    details: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True


class CorrelationResponse(BaseModel):
    id: str
    dataset_id: str
    var1: str
    var2: str
    pearson_r: float
    p_value: float
    interpretation: str
    created_at: datetime

    class Config:
        from_attributes = True


class ClaimCreate(BaseModel):
    title: str
    description: str
    supporting_data: Optional[Dict[str, Any]] = None


class ClaimResponse(BaseModel):
    id: str
    title: str
    description: str
    state: str
    supporting_data: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EvidenceGateResponse(BaseModel):
    id: str
    claim_id: str
    gate_name: str
    status: str
    evidence_details: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogResponse(BaseModel):
    id: str
    action: str
    actor: str
    resource_type: str
    resource_id: str
    details: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True
