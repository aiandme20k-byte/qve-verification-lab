# QVE Project v2.3 — Codex Build Baseline

This branch is a UI/verification-lab evolution of Prototype 1. It adds an aerospace mission-control visual layer around the existing evidence-ledger, deterministic analysis, and 3D digital-twin concepts.

## Scope
- QVE spacecraft reference geometry as a MODEL / SIMULATION visualization.
- D1 laboratory verification workflow and telemetry dashboard.
- English + Myanmar UI entry points.
- Evidence-state separation: MODEL, SIMULATED, ACTUAL_DATA, CALCULATED, INCONCLUSIVE, VERIFIED.
- Existing CSV/JSON intake, SHA-256 hashing, QC, physics calculations, digital twin, audit concepts remain the scientific backbone.

## Important truth boundary
The spacecraft visuals, telemetry values, and flight-style panels are interface/demo content unless backed by a real instrument record. They do not establish propulsion, vacuum-energy extraction, warp drive, flight readiness, or human-rated capability.

## Local run
```bash
cd qve-verification-lab/frontend
npm install
npm run build
npm run dev
```

Backend remains available under `qve-verification-lab/backend` using the existing FastAPI instructions.

## Next Codex work package
1. Replace CSS ship silhouette with a licensed/imported GLTF/GLB model supplied by the project owner.
2. Add real Three.js camera controls, measurement overlays, coordinate frames, and selectable subsystems.
3. Add telemetry schema + WebSocket replay with explicit SIMULATED/ACTUAL_DATA provenance.
4. Complete evidence, QC, replay, report, and audit screens instead of placeholders.
5. Add Myanmar translations using Unicode-safe fonts and fallbacks.
6. Add automated frontend/backend tests and a CI build gate.
7. Deploy the frontend through a user-controlled hosting provider; GitHub repository alone is source hosting, not a guaranteed public application URL.
