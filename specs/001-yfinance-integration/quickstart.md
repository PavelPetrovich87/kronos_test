# Quickstart: Using yfinance DataLoader

## Installation

Ensure `yfinance` is installed:

```bash
pip install -r requirements.txt
```

## Usage

The `DataLoader` now supports automatic fetching. You do not need to manually download CSVs.

```python
from lib.data_loader import DataLoader

loader = DataLoader(data_dir="data")

# This will:
# 1. Check if data/AAPL_1d.csv exists.
# 2. If NOT, download from Yahoo Finance.
# 3. Save to data/AAPL_1d.csv.
# 4. Return the DataFrame.
df = loader.load_ohlcv("AAPL", "1d")

print(df.head())
```

## Troubleshooting

- **FileNotFoundError**: Should not happen for valid symbols unless network is down.
- **Empty DataFrame**: Symbol might be delisted or invalid date range.
- **Rate Limits**: If you loop through 500 symbols rapidly, Yahoo checks might fail. Add `time.sleep(1)` between calls.
