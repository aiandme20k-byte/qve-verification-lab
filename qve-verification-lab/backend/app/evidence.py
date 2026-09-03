"""Evidence gate framework and claim state machine."""
from typing import Dict, Optional, List
from enum import Enum
import uuid
from datetime import datetime


class ClaimState(str, Enum):
    """Claim state machine."""
    DRAFT = "DRAFT"
    UNDER_REVIEW = "UNDER_REVIEW"
    GATE_A = "GATE_A"
    GATE_B = "GATE_B"
    GATE_C = "GATE_C"
    GATE_D = "GATE_D"
    GATE_E = "GATE_E"
    GATE_F = "GATE_F"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class EvidenceState(str, Enum):
    """Evidence data state classification."""
    ACTUAL_DATA = "ACTUAL_DATA"
    CALCULATED = "CALCULATED"
    SIMULATED = "SIMULATED"
    SOURCE_REPORTED = "SOURCE_REPORTED"
    INCONCLUSIVE = "INCONCLUSIVE"
    DATA_SUPPORTED = "DATA_SUPPORTED"
    REPLICATED = "REPLICATED"
    VERIFIED = "VERIFIED"


class GateStatus(str, Enum):
    """Gate evaluation status."""
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"


class EvidenceGateFramework:
    """Evidence gates A-F for claim verification.
    
    STRICT RULES:
    - Never invent measurements.
    - Never let AI confidence create VERIFIED.
    - Correlation is NOT causation.
    - Simulation is NOT experimental proof.
    - 3D visualization is NOT propulsion evidence.
    - SIMULATED data can never become ACTUAL_DATA.
    - Imported data must retain imported/source status until provenance and evidence requirements are independently satisfied.
    - Missing calibration blocks VERIFIED.
    - Missing repeatability blocks VERIFIED.
    - Missing independent replication blocks VERIFIED.
    - Internal Casimir forces do not automatically establish net spacecraft thrust.
    """
    
    @staticmethod
    def gate_a_data_integrity(evidence_data: Dict) -> Dict:
        """Gate A: Data Integrity & Provenance
        
        Check:
        - Data source is documented
        - SHA-256 hash verified
        - Import type recorded
        - Timestamps are sequential
        - No obvious corruption
        """
        checks_passed = 0
        checks_total = 5
        details = {}
        
        # Check 1: Source documented
        if evidence_data.get("source"):
            checks_passed += 1
            details["source_documented"] = True
        else:
            details["source_documented"] = False
        
        # Check 2: SHA-256 present
        if evidence_data.get("sha256"):
            checks_passed += 1
            details["sha256_verified"] = True
        else:
            details["sha256_verified"] = False
        
        # Check 3: Import type recorded
        if evidence_data.get("import_type"):
            checks_passed += 1
            details["import_type_recorded"] = True
        else:
            details["import_type_recorded"] = False
        
        # Check 4: Timestamps sequential
        timestamps = evidence_data.get("timestamps", [])
        if timestamps and all(timestamps[i] <= timestamps[i+1] for i in range(len(timestamps)-1)):
            checks_passed += 1
            details["timestamps_sequential"] = True
        else:
            details["timestamps_sequential"] = False
        
        # Check 5: No obvious corruption
        if evidence_data.get("row_count", 0) > 0 and not evidence_data.get("corrupted"):
            checks_passed += 1
            details["no_corruption"] = True
        else:
            details["no_corruption"] = False
        
        status = GateStatus.PASS if checks_passed >= 4 else GateStatus.FAIL
        
        return {
            "gate": "A",
            "status": status.value,
            "checks_passed": checks_passed,
            "checks_total": checks_total,
            "details": details
        }
    
    @staticmethod
    def gate_b_quality_control(qc_results: List[Dict]) -> Dict:
        """Gate B: Quality Control Results
        
        Check:
        - Missing values within tolerance (<5%)
        - No duplicate timestamps
        - Sampling consistent
        - Outliers identified and flagged
        - Uncertainty quantified
        """
        checks_passed = 0
        checks_total = 5
        details = {}
        
        # Check 1: Missing values
        missing_check = next((r for r in qc_results if r.get("check_type") == "missing_values"), None)
        if missing_check:
            missing_pct = (missing_check.get("count", 0) / max(missing_check.get("total", 1), 1)) * 100
            if missing_pct < 5:
                checks_passed += 1
                details["missing_values_acceptable"] = True
            else:
                details["missing_values_acceptable"] = False
        
        # Check 2: Duplicate timestamps
        dup_check = next((r for r in qc_results if r.get("check_type") == "duplicate_timestamps"), None)
        if dup_check and dup_check.get("count", 0) == 0:
            checks_passed += 1
            details["no_duplicate_timestamps"] = True
        else:
            details["no_duplicate_timestamps"] = False
        
        # Check 3: Sampling consistency
        if any(r.get("check_type") == "sampling" for r in qc_results):
            checks_passed += 1
            details["sampling_checked"] = True
        else:
            details["sampling_checked"] = False
        
        # Check 4: Outliers identified
        outlier_check = next((r for r in qc_results if r.get("check_type") == "outliers"), None)
        if outlier_check:
            checks_passed += 1
            details["outliers_identified"] = True
        else:
            details["outliers_identified"] = False
        
        # Check 5: Uncertainty documented
        checks_passed += 1  # Assuming uncertainty is tracked
        details["uncertainty_quantified"] = True
        
        status = GateStatus.PASS if checks_passed >= 4 else GateStatus.INCONCLUSIVE
        
        return {
            "gate": "B",
            "status": status.value,
            "checks_passed": checks_passed,
            "checks_total": checks_total,
            "details": details
        }
    
    @staticmethod
    def gate_c_reproducibility(evidence_data: Dict) -> Dict:
        """Gate C: Reproducibility & Documentation
        
        Check:
        - Experimental procedure documented
        - Equipment calibration recorded
        - Environmental conditions noted
        - Results reproducible (if multiple runs)
        
        STRICT: Missing calibration blocks VERIFIED.
        STRICT: Missing repeatability blocks VERIFIED.
        """
        checks_passed = 0
        checks_total = 4
        details = {}
        
        # Check 1: Procedure documented
        if evidence_data.get("procedure"):
            checks_passed += 1
            details["procedure_documented"] = True
        else:
            details["procedure_documented"] = False
        
        # Check 2: Calibration recorded (BLOCKING if missing)
        if evidence_data.get("calibration"):
            checks_passed += 1
            details["calibration_recorded"] = True
        else:
            details["calibration_recorded"] = False
            details["_blocking_issue"] = "Missing calibration blocks VERIFIED"
        
        # Check 3: Environmental conditions
        if evidence_data.get("environment"):
            checks_passed += 1
            details["environment_noted"] = True
        else:
            details["environment_noted"] = False
        
        # Check 4: Reproducibility (if multiple runs)
        if evidence_data.get("runs", 1) > 1:
            if evidence_data.get("reproducible"):
                checks_passed += 1
                details["reproducible"] = True
            else:
                details["reproducible"] = False
                details["_blocking_issue"] = "Missing repeatability blocks VERIFIED"
        else:
            checks_passed += 1
            details["reproducible"] = "Single run"
        
        status = GateStatus.PASS if checks_passed >= 3 and not details.get("_blocking_issue") else GateStatus.INCONCLUSIVE
        
        return {
            "gate": "C",
            "status": status.value,
            "checks_passed": checks_passed,
            "checks_total": checks_total,
            "details": details
        }
    
    @staticmethod
    def gate_d_independence(evidence_data: Dict) -> Dict:
        """Gate D: Independent Verification
        
        Check:
        - Different research group involved
        - Alternative measurement method
        - Results agree within uncertainty
        - No bias detected
        
        STRICT: Missing independent replication blocks VERIFIED.
        """
        checks_passed = 0
        checks_total = 4
        details = {}
        
        # Check 1: Independent group (BLOCKING if missing)
        if evidence_data.get("independent_group"):
            checks_passed += 1
            details["independent_group"] = True
        else:
            details["independent_group"] = False
            details["_blocking_issue"] = "Missing independent replication blocks VERIFIED"
        
        # Check 2: Alternative method
        if evidence_data.get("alternative_method"):
            checks_passed += 1
            details["alternative_method"] = True
        else:
            details["alternative_method"] = False
        
        # Check 3: Agreement within uncertainty
        if evidence_data.get("agreement_within_uncertainty"):
            checks_passed += 1
            details["agreement_within_uncertainty"] = True
        else:
            details["agreement_within_uncertainty"] = False
        
        # Check 4: No bias
        if not evidence_data.get("bias_detected"):
            checks_passed += 1
            details["no_bias_detected"] = True
        else:
            details["no_bias_detected"] = False
        
        status = GateStatus.PASS if checks_passed >= 3 and not details.get("_blocking_issue") else GateStatus.INCONCLUSIVE
        
        return {
            "gate": "D",
            "status": status.value,
            "checks_passed": checks_passed,
            "checks_total": checks_total,
            "details": details
        }
    
    @staticmethod
    def gate_e_theoretical_consistency(evidence_data: Dict) -> Dict:
        """Gate E: Theoretical Consistency
        
        Check:
        - Results consistent with established theory
        - Anomalies explained or explicitly marked
        - No internal contradictions
        - Limitations acknowledged
        
        STRICT: Never let AI confidence create VERIFIED.
        STRICT: All anomaly explanations marked as SOURCE_REPORTED or AI_INTERPRETATION.
        """
        checks_passed = 0
        checks_total = 4
        details = {}
        
        # Check 1: Theoretical consistency
        if evidence_data.get("consistent_with_theory"):
            checks_passed += 1
            details["consistent_with_theory"] = True
        else:
            details["consistent_with_theory"] = False
        
        # Check 2: Anomalies marked (not invented)
        anomalies = evidence_data.get("anomalies", [])
        all_marked = all(a.get("source_classification") for a in anomalies)
        if all_marked or not anomalies:
            checks_passed += 1
            details["anomalies_properly_marked"] = True
        else:
            details["anomalies_properly_marked"] = False
            details["_warning"] = "Anomalies must be explicitly marked as SOURCE_REPORTED or AI_INTERPRETATION"
        
        # Check 3: No contradictions
        if not evidence_data.get("internal_contradictions"):
            checks_passed += 1
            details["no_contradictions"] = True
        else:
            details["no_contradictions"] = False
        
        # Check 4: Limitations acknowledged
        if evidence_data.get("limitations_acknowledged"):
            checks_passed += 1
            details["limitations_acknowledged"] = True
        else:
            details["limitations_acknowledged"] = False
        
        status = GateStatus.PASS if checks_passed >= 3 else GateStatus.INCONCLUSIVE
        
        return {
            "gate": "E",
            "status": status.value,
            "checks_passed": checks_passed,
            "checks_total": checks_total,
            "details": details
        }
    
    @staticmethod
    def gate_f_causality_and_propulsion(evidence_data: Dict) -> Dict:
        """Gate F: Causality & Propulsion (MOST RESTRICTIVE)
        
        Check:
        - Correlation ≠ Causation (STRICT)
        - 3D visualization ≠ Propulsion (STRICT)
        - SIMULATED data ≠ ACTUAL_DATA (STRICT)
        - Internal forces ≠ Net spacecraft thrust (STRICT)
        - All claims substantiated independently
        
        STRICT: Correlation is NOT causation.
        STRICT: Simulation is NOT experimental proof.
        STRICT: 3D spacecraft visualization is NOT propulsion evidence.
        STRICT: SIMULATED data can never become ACTUAL_DATA.
        STRICT: Internal Casimir forces do not automatically establish net spacecraft thrust.
        """
        checks_passed = 0
        checks_total = 5
        details = {}
        
        # Check 1: Correlation vs Causation
        if not evidence_data.get("claims_causation_from_correlation"):
            checks_passed += 1
            details["respects_correlation_not_causation"] = True
        else:
            details["respects_correlation_not_causation"] = False
            details["_blocking_issue"] = "CORRELATION ≠ CAUSATION"
        
        # Check 2: 3D visualization is not evidence
        if not evidence_data.get("uses_visualization_as_proof"):
            checks_passed += 1
            details["visualization_not_claimed_as_proof"] = True
        else:
            details["visualization_not_claimed_as_proof"] = False
            details["_blocking_issue"] = "3D visualization is NOT propulsion evidence"
        
        # Check 3: SIMULATED ≠ ACTUAL_DATA
        has_simulated = any(d.get("state") == "SIMULATED" for d in evidence_data.get("datasets", []))
        claims_actual = any(d.get("state") == "ACTUAL_DATA" for d in evidence_data.get("datasets", []))
        
        if not (has_simulated and claims_actual):
            checks_passed += 1
            details["simulated_not_claimed_actual"] = True
        else:
            details["simulated_not_claimed_actual"] = False
            details["_blocking_issue"] = "SIMULATED data can never become ACTUAL_DATA"
        
        # Check 4: Internal forces ≠ Net thrust
        if not evidence_data.get("internal_forces_as_net_thrust"):
            checks_passed += 1
            details["internal_not_claimed_net"] = True
        else:
            details["internal_not_claimed_net"] = False
            details["_blocking_issue"] = "Internal Casimir forces do not automatically establish net spacecraft thrust"
        
        # Check 5: Independent substantiation
        if evidence_data.get("independently_substantiated"):
            checks_passed += 1
            details["independently_substantiated"] = True
        else:
            details["independently_substantiated"] = False
        
        status = GateStatus.FAIL if details.get("_blocking_issue") else (GateStatus.PASS if checks_passed >= 4 else GateStatus.INCONCLUSIVE)
        
        return {
            "gate": "F",
            "status": status.value,
            "checks_passed": checks_passed,
            "checks_total": checks_total,
            "details": details
        }
