"""Scientific analysis and computation functions."""
import hashlib
import csv
import json
from typing import List, Dict, Tuple, Optional
import numpy as np
from scipy import stats
import pandas as pd
import uuid
from datetime import datetime


def compute_sha256(filepath: str) -> str:
    """Compute SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def import_csv(filepath: str) -> Tuple[List[Dict], str, int]:
    """Import CSV file and return records."""
    records = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        records = list(reader)
    sha256 = compute_sha256(filepath)
    return records, sha256, len(records)


def import_json(filepath: str) -> Tuple[List[Dict], str, int]:
    """Import JSON file and return records."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    if not isinstance(data, list):
        data = [data]
    sha256 = compute_sha256(filepath)
    return data, sha256, len(data)


def check_missing_values(records: List[Dict]) -> Dict:
    """Check for missing values in dataset."""
    if not records:
        return {"status": "FAIL", "missing_count": 0, "affected_fields": []}
    
    missing_by_field = {}
    for record in records:
        for key, value in record.items():
            if value is None or value == "" or value.lower() == "nan":
                if key not in missing_by_field:
                    missing_by_field[key] = 0
                missing_by_field[key] += 1
    
    missing_count = sum(missing_by_field.values())
    status = "PASS" if missing_count == 0 else "WARNING"
    
    return {
        "status": status,
        "missing_count": missing_count,
        "affected_fields": missing_by_field
    }


def check_duplicate_timestamps(records: List[Dict], timestamp_field: str = "timestamp") -> Dict:
    """Check for duplicate timestamps in dataset."""
    if not records:
        return {"status": "PASS", "duplicate_count": 0}
    
    timestamps = []
    for record in records:
        if timestamp_field in record:
            try:
                ts = float(record[timestamp_field])
                timestamps.append(ts)
            except:
                pass
    
    if not timestamps:
        return {"status": "PASS", "duplicate_count": 0}
    
    duplicates = len(timestamps) - len(set(timestamps))
    status = "PASS" if duplicates == 0 else "WARNING"
    
    return {
        "status": status,
        "duplicate_count": duplicates,
        "total_records": len(records)
    }


def check_outliers(values: List[float], threshold: float = 3.0) -> Dict:
    """Detect outliers using z-score method."""
    if not values or len(values) < 3:
        return {"status": "PASS", "outlier_count": 0, "indices": []}
    
    values_array = np.array(values)
    z_scores = np.abs(stats.zscore(values_array))
    outlier_indices = np.where(z_scores > threshold)[0].tolist()
    
    status = "PASS" if len(outlier_indices) == 0 else "WARNING"
    
    return {
        "status": status,
        "outlier_count": len(outlier_indices),
        "indices": outlier_indices,
        "threshold": threshold
    }


def calculate_pearson_correlation(var1: List[float], var2: List[float]) -> Tuple[float, float]:
    """Calculate Pearson correlation coefficient.
    
    IMPORTANT: Correlation ≠ Causation
    This result is MARKED as NOT CAUSATION.
    """
    if not var1 or not var2 or len(var1) != len(var2):
        return 0.0, 1.0
    
    try:
        var1_array = np.array([float(v) for v in var1 if v is not None])
        var2_array = np.array([float(v) for v in var2 if v is not None])
        
        if len(var1_array) < 2 or len(var2_array) < 2:
            return 0.0, 1.0
        
        r, p_value = stats.pearsonr(var1_array, var2_array)
        return float(r), float(p_value)
    except:
        return 0.0, 1.0


def calculate_casimir_force(area_m2: float, gap_nm: float) -> float:
    """Calculate ideal Casimir force (deterministic, not proof of propulsion).
    
    Formula: F = (π² * ℏ * c * A) / (240 * d⁴)
    
    WARNING: This is CALCULATED theoretical force.
    SIMULATED data can never become ACTUAL_DATA.
    Internal Casimir forces do not automatically establish net spacecraft thrust.
    """
    hbar = 1.054571817e-34  # J⋅s (reduced Planck constant)
    c = 299792458  # m/s (speed of light)
    
    if gap_nm <= 0 or area_m2 <= 0:
        return 0.0
    
    gap_m = gap_nm * 1e-9  # Convert nm to m
    
    # Force in Newtons
    force = (np.pi**2 * hbar * c * area_m2) / (240 * gap_m**4)
    return float(force)


def calculate_radiation_momentum(energy_joules: float) -> float:
    """Calculate radiation momentum (deterministic).
    
    Formula: p = E / c
    
    WARNING: This is theoretical momentum.
    NOT proof of spacecraft propulsion.
    """
    c = 299792458  # m/s
    
    if energy_joules <= 0:
        return 0.0
    
    momentum = energy_joules / c
    return float(momentum)


def calculate_uncertainty_propagation(values: List[float], operation: str = "std") -> float:
    """Calculate uncertainty using standard deviation."""
    if not values or len(values) < 2:
        return 0.0
    
    values_array = np.array([float(v) for v in values if v is not None])
    
    if operation == "std":
        return float(np.std(values_array))
    elif operation == "sem":
        return float(stats.sem(values_array))
    
    return 0.0


def energy_accounting(power_watts: List[float], time_seconds: List[float]) -> Dict:
    """Calculate total energy from power measurements.
    
    E = ∫ P(t) dt (approximated as trapezoidal integration)
    """
    if not power_watts or not time_seconds or len(power_watts) != len(time_seconds):
        return {"total_energy_joules": 0.0, "method": "trapz"}
    
    try:
        power_array = np.array([float(p) for p in power_watts if p is not None])
        time_array = np.array([float(t) for t in time_seconds if t is not None])
        
        if len(power_array) < 2:
            return {"total_energy_joules": 0.0, "method": "trapz"}
        
        energy = float(np.trapz(power_array, time_array))
        return {"total_energy_joules": energy, "method": "trapz"}
    except:
        return {"total_energy_joules": 0.0, "method": "trapz"}
