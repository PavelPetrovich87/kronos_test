# Research: yfinance Integration

**Date**: 2026-01-14
**Feature**: yfinance Integration

## Decisions

### 1. Library Selection
- **Decision**: Use `yfinance` library.
- **Rationale**: Standard, widely used, zero-config API for Yahoo Finance. Support for "sane" downloading of OHLCV data. 
- **Alternatives**: `alpha_vantage` (requires key), `ccxt` (crypto focussed, but we might want stocks/forex too).

### 2. Data fetching method
- **Decision**: Use `yf.Ticker(symbol).history(period="10y", interval=timeframe)`
- **Rationale**: `Ticker` object provides more granular control and metadata if needed later compared to `yf.download`.
- **Note**: `1h` timeframe has limitation on how far back history goes (730 days). We will accept default limitations for now.

### 3. Normalization
- **Decision**: Explicitly rename columns to `['open', 'high', 'low', 'close', 'volume']` using lower-case.
- **Rationale**: `yfinance` returns `['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']`. Kronos expects lowercase. We'll drop non-OHLCV columns for now to keep it simple as per spec.

### 4. Dependency Management
- **Decision**: Add `yfinance` to `requirements.txt`.
- **Rationale**: Hard requirement.

## Unknowns Analysis

- **Unknown**: Rate limiting?
- **Finding**: Yahoo Finance has dynamic rate limiting. `yfinance` handles simple retries, but we should wrap in a basic try/catch or assume the user won't spam loops immediately.
- **Resolution**: Implementation will include basic exception handling (FR-006).

## Best Practices

- Cache-first: Always check disk before network (as per Spec FR-002).
- Data Immutability: Once written to CSV, we treat it as "raw". Re-fetching requires manual deletion (or specific "force" flag, but spec says check existence).
