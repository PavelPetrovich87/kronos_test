# Data Model: Market Data

**Feature**: yfinance Integration

## Storage format

- **Type**: CSV Files
- **Location**: `data/{symbol}_{timeframe}.csv` (relative to configured data dir)
- **Immutability**: Files are write-once. Updates require deletion or distinct versioning (out of scope for now).

## Schema

| Column | Type | Description |
|--------|------|-------------|
| timestamp | datetime | Index. ISO 8601 formatted or standard pandas timestamp string. |
| open | float | Opening price |
| high | float | Highest price |
| low | float | Lowest price |
| close | float | Closing price |
| volume | float/int | Trading volume |

## Validation Rules

1. **Columns**: Must contain exactly the lowercase columns above. Extra columns from source are dropped.
2. **Types**: OHLC must be numeric.
3. **Index**: Must be convertible to `DatetimeIndex`.
