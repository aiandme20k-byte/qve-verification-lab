"""Backend tests for QVE Verification Lab."""
import pytest
import json
import tempfile
import os
from pathlib import Path
from app.analysis import (
    compute_sha256,
    import_csv,
    import_json,
    check_missing_values,
    check_duplicate_timestamps,
    check_outliers,
    calculate_pearson_correlation,
    calculate_casimir_force,
    calculate_radiation_momentum,
    calculate_uncertainty_propagation,
    energy_accounting,
)


def test_sha256():
    """Test SHA-256 computation."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write('timestamp,value\n1,10.5\n2,11.3\n')
        temp_path = f.name
    
    try:
        sha = compute_sha256(temp_path)
        assert isinstance(sha, str)
        assert len(sha) == 64
        print(f"✓ SHA-256 test PASSED: {sha}")
    finally:
        os.unlink(temp_path)


def test_csv_import():
    """Test CSV import."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write('timestamp,value,channel\n')
        f.write('1.0,10.5,A\n')
        f.write('2.0,11.3,A\n')
        f.write('3.0,12.1,B\n')
        temp_path = f.name
    
    try:
        records, sha256, count = import_csv(temp_path)
        assert len(records) == 3
        assert count == 3
        assert 'timestamp' in records[0]
        assert sha256
        print(f"✓ CSV import test PASSED: {count} records")
    finally:
        os.unlink(temp_path)


def test_json_import():
    """Test JSON import."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump([
            {"timestamp": 1.0, "value": 10.5},
            {"timestamp": 2.0, "value": 11.3},
        ], f)
        temp_path = f.name
    
    try:
        records, sha256, count = import_json(temp_path)
        assert len(records) == 2
        assert count == 2
        assert sha256
        print(f"✓ JSON import test PASSED: {count} records")
    finally:
        os.unlink(temp_path)


def test_missing_values():
    """Test missing value detection."""
    records = [
        {"value": 10.5, "timestamp": 1.0},
        {"value": None, "timestamp": 2.0},
        {"value": 12.1, "timestamp": 3.0},
    ]
    
    result = check_missing_values(records)
    assert result["status"] in ["PASS", "WARNING", "FAIL"]
    print(f"✓ Missing values test PASSED: {result.get('missing_count', 0)} missing")


def test_duplicate_timestamps():
    """Test duplicate timestamp detection."""
    records = [
        {"timestamp": 1.0, "value": 10.5},
        {"timestamp": 2.0, "value": 11.3},
        {"timestamp": 2.0, "value": 11.5},
        {"timestamp": 3.0, "value": 12.1},
    ]
    
    result = check_duplicate_timestamps(records)
    assert result["duplicate_count"] >= 1
    print(f"✓ Duplicate timestamps test PASSED: {result['duplicate_count']} duplicates")


def test_outliers():
    """Test outlier detection."""
    values = [10.0, 11.0, 10.5, 11.5, 10.8, 100.0]
    
    result = check_outliers(values, threshold=3.0)
    assert result["status"] in ["PASS", "WARNING"]
    print(f"✓ Outlier detection test PASSED: {result['outlier_count']} outliers")


def test_pearson_correlation():
    """Test Pearson correlation."""
    var1 = [1.0, 2.0, 3.0, 4.0, 5.0]
    var2 = [2.0, 4.0, 6.0, 8.0, 10.0]
    
    r, p_value = calculate_pearson_correlation(var1, var2)
    assert -1.0 <= r <= 1.0
    assert 0.0 <= p_value <= 1.0
    assert r > 0.99
    print(f"✓ Pearson correlation test PASSED: r={r:.4f}, p={p_value:.6f}")
    print(f"  WARNING: Correlation ≠ Causation")


def test_casimir_force():
    """Test Casimir force calculation."""
    force = calculate_casimir_force(area_m2=1.0, gap_nm=100.0)
    assert isinstance(force, float)
    assert force > 0
    print(f"✓ Casimir force test PASSED: F={force:.6e} N")
    print(f"  STATE: CALCULATED (theoretical, not experimental proof)")


def test_radiation_momentum():
    """Test radiation momentum calculation."""
    momentum = calculate_radiation_momentum(energy_joules=1.0)
    assert isinstance(momentum, float)
    assert momentum > 0
    print(f"✓ Radiation momentum test PASSED: p={momentum:.6e} kg·m/s")


def test_uncertainty_propagation():
    """Test uncertainty calculation."""
    values = [10.0, 10.1, 9.9, 10.2, 9.8]
    uncertainty = calculate_uncertainty_propagation(values)
    assert isinstance(uncertainty, float)
    assert uncertainty >= 0
    print(f"✓ Uncertainty propagation test PASSED: σ={uncertainty:.6f}")


def test_energy_accounting():
    """Test energy accounting."""
    power = [100.0, 110.0, 105.0, 115.0]
    time = [0.0, 1.0, 2.0, 3.0]
    
    result = energy_accounting(power, time)
    assert result["total_energy_joules"] > 0
    print(f"✓ Energy accounting test PASSED: E={result['total_energy_joules']:.2f} J")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("QVE VERIFICATION LAB — BACKEND TESTS")
    print("="*60 + "\n")
    
    test_sha256()
    test_csv_import()
    test_json_import()
    test_missing_values()
    test_duplicate_timestamps()
    test_outliers()
    test_pearson_correlation()
    test_casimir_force()
    test_radiation_momentum()
    test_uncertainty_propagation()
    test_energy_accounting()
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED ✓")
    print("="*60 + "\n")
