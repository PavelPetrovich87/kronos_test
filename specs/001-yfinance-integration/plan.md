# Implementation Plan: yfinance Integration

**Branch**: `001-yfinance-integration` | **Date**: 2026-01-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-yfinance-integration/spec.md`

## Summary

Integrate `yfinance` into `DataLoader` to automatically fetch and cache OHLCV market data when local files are missing. This removes the need for manual CSV management.

## Technical Context

**Language/Version**: Python 3.x
**Primary Dependencies**: `yfinance` (new), `pandas` (existing)
**Storage**: CSV files in `data/` directory
**Testing**: `pytest` (to be added) or `unittest`
**Target Platform**: Local execution (macOS/Linux)
**Project Type**: Python Library/Scripts

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Reproducible Notebooks**: N/A (Lib change)
- [x] **Data Immutability**: Respected. We only write new files if they don't exist. We do not overwrite.
- [x] **Modular Components**: implementation is in `lib/data_loader.py`.
- [x] **Standardized Layout**: Data goes to `data/`.

## Proposed Changes

### Configuration
#### [MODIFY] [requirements.txt](file:///Users/macintoshhd/WebstormProjects/kronos_test/requirements.txt)
- Add `yfinance`
- Add `pytest` (for testing)

### Library
#### [MODIFY] [data_loader.py](file:///Users/macintoshhd/WebstormProjects/kronos_test/lib/data_loader.py)
- Import `yfinance`.
- In `load_ohlcv`:
    - Check if file exists.
    - If no:
        - Call `yf.Ticker(symbol).history(...)`
        - Normalize columns (rename to lower case).
        - Save to CSV using `save_raw` or direct pandas to_csv.
    - If yes: load as usual.

### Testing
#### [NEW] [test_data_loader.py](file:///Users/macintoshhd/WebstormProjects/kronos_test/tests/test_data_loader.py)
- Test `load_ohlcv` with a mock `yfinance` (to avoid network in unit tests).
- Test `load_ohlcv` integration (real fetch) - marked as slow or integration.

## Verification Plan

### Automated Tests
Run the new tests:
```bash
# Install dependencies first
pip install -r requirements.txt
# Run tests
pytest tests/test_data_loader.py
```

### Manual Verification
Create a script `verify_yfinance.py`:
```python
from lib.data_loader import DataLoader
import os

# Ensure clean slate
if os.path.exists("data/AAPL_1d.csv"):
    os.remove("data/AAPL_1d.csv")

loader = DataLoader()
df = loader.load_ohlcv("AAPL", "1d")
print("Fetched shape:", df.shape)
print("Columns:", df.columns)

assert not df.empty
assert 'close' in df.columns
assert os.path.exists("data/AAPL_1d.csv")
print("Verification Success!")
```
