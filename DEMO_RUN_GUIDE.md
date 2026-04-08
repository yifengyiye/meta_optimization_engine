# Demo Run Guide

## Files

- Input payload: [sample_payload.json](D:\agent\meta_agent\meta_optimization_engine\sample_payload.json)
- Expected output: [sample_expected_output.json](D:\agent\meta_agent\meta_optimization_engine\sample_expected_output.json)

## Start API

```bash
cd D:\agent\meta_agent\meta_optimization_engine
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000/docs`

## Run With cURL

```bash
curl -X POST "http://127.0.0.1:8000/analyze" ^
  -H "Content-Type: application/json" ^
  --data "@sample_payload.json"
```

## Run With PowerShell

```powershell
$payload = Get-Content -LiteralPath '.\\sample_payload.json' -Raw
Invoke-RestMethod `
  -Method Post `
  -Uri 'http://127.0.0.1:8000/analyze' `
  -ContentType 'application/json' `
  -Body $payload
```

## What To Expect

The sample input is designed to trigger four typical outcomes:

1. `ad_demo_low_ctr`
   - Main result: `PAUSE`
   - Reason: click layer too weak

2. `ad_demo_lpv_issue`
   - Main result: `FIX_LANDING_PAGE`
   - Reason: strong click layer but weak LPV rate

3. `ad_demo_checkout_issue`
   - Main result: `FIX_TRACKING` or `FIX_CHECKOUT`
   - Reason: checkout exists but purchases are zero

4. `ad_demo_good_scale`
   - Main result: `SCALE`
   - Reason: stable profitability with room to expand

## Notes

- `sample_expected_output.json` is a reference example, not a strict snapshot
- Exact matched rules can change as the YAML rule set evolves
- The primary action and diagnosis summary should stay directionally consistent

