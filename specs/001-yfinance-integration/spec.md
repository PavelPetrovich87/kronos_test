# Feature Specification: yfinance Integration

**Feature Branch**: `001-yfinance-integration`  
**Created**: 2026-01-14  
**Status**: Draft  
**Input**: User description: "We need to implement the integration of yfinance library so our DataLoader uses it"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Auto-fetch Missing Data (Priority: P1)

As a researcher or trader, I want the system to automatically fetch market data from Yahoo Finance when it's not available locally, so that I don't have to manually download and format CSV files.

**Why this priority**: Removes friction in getting started with new symbols and enables rapid testing.

**Independent Test**: Can be tested by deleting local data for a common symbol (e.g., "SPY") and requesting it via `DataLoader`.

**Acceptance Scenarios**:

1. **Given** no local data for "MSG" (Meta), **When** `load_ohlcv("MSG", "1d")` is called, **Then** the system downloads data from Yahoo Finance, saves it to disk, and returns the DataFrame.
2. **Given** invalid symbol "INVALID_SYM", **When** `load_ohlcv` is called, **Then** the system raises an appropriate error (e.g., FileNotFoundError or specialized data error) after attempting fetch.

---

### User Story 2 - Data Normalization (Priority: P1)

As a developer, I need fetched data to be standardized to the system's expected schema (lowercase columns, datetime index), so that downstream components (Backtester, Feature Engineering) work without modification.

**Why this priority**: Ensures zero-config compatibility with the rest of the Kronos system.

**Independent Test**: Inspect the DataFrame returned from a fresh download.

**Acceptance Scenarios**:

1. **Given** data fetched from yfinance, **When** returned by `DataLoader`, **Then** columns include ['open', 'high', 'low', 'close', 'volume'] in lowercase.
2. **Given** data fetched from yfinance, **When** returned, **Then** the index is a `DatetimeIndex` with correct timezone info (usually UTC or naive, matching system convention).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST integrate the `yfinance` library to fetch historical market data.
- **FR-002**: `DataLoader.load_ohlcv` MUST check for the existence of a local file first (Cache-First strategy).
- **FR-003**: If local data is missing, System MUST attempt to download the data using `yfinance` for the specified symbol and timeframe.
- **FR-004**: System MUST normalize the downloaded data columns to match the internal schema: `open`, `high`, `low`, `close`, `volume`.
- **FR-005**: System MUST persist the downloaded and normalized data to the configured `data_dir` as a CSV file to avoid re-fetching on subsequent runs.
- **FR-006**: System MUST handle network errors or invalid symbol errors gracefully (raising meaningful exceptions).

### Key Entities

- **DataLoader**: The existing class responsible for I/O. Will be enhanced with fetching capabilities.
- **yfinance.Ticker**: External entity used to interface with Yahoo Finance API.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully load a new symbol (e.g., 'AAPL') in under 10 seconds (assuming standard network speed) without manual file creation.
- **SC-002**: 100% of fetched DataFrames match the required schema (index: Datetime, columns: ohlcv).
- **SC-003**: Subsequent requests for the same symbol/timeframe load from disk (milliseconds execution time) rather than network.
