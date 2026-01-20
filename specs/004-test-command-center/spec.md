# Feature Specification: Test Command Center

**Feature Branch**: `004-test-command-center`  
**Created**: 2026-01-20  
**Status**: Draft  
**Input**: User description: "Create a proper notebook, that can visualize test results, where we can setup different test related settings period etc. Tables, outcomes. A test command center."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Interactive Visualization (Priority: P1)

As a Quantitative Researcher, I want to visualize my backtest results (Equity Curve, Drawdowns, and Signals) in a graphical format so that I can quickly understand the strategy's behavior across time.

**Why this priority**: A picture is worth a thousand CSV logs. Visualization is critical for identifying "overfitting" or weird model behavior that metrics might miss.

**Independent Test**: Can be tested by executing the visualization cells in the notebook after a run and confirming that charts (Plotly/Matplotlib) are rendered correctly.

**Acceptance Scenarios**:

1. **Given** a completed backtest run, **When** the visualization cell is run, **Then** an Equity Curve chart is displayed comparing Strategy vs. Buy & Hold.
2. **Given** a set of generated signals, **When** viewing the Price Chart, **Then** Long/Short markers are correctly overlaid on the price candles/lines.

---

### User Story 2 - Parametric Test Control (Priority: P1)

As a Researcher, I want to define my test constraints (date range, symbol, transaction fees) within the notebook UI so that I don't have to modify the underlying Python library for every experiment.

**Why this priority**: Enables rapid experimentation. Without this, the "Command Center" is just a static report rather than a "Center".

**Independent Test**: Can be tested by changing the `START_DATE` or `MODE` variable in the notebook and verifying the output signals change accordingly.

**Acceptance Scenarios**:

1. **Given** a configured start date of "2023-01-01", **When** the data is loaded, **Then** only bars from that date onwards are processed.
2. **Given** a choice between "Mock" and "Real" model modes, **When** the backtest is triggered, **Then** the `StrategyFactory` instantiates the correct predictor.

---

### User Story 3 - Outcome Audit Tables (Priority: P2)

As a Developer, I want to see a detailed table of every trade executed and a final performance scorecard so that I can verify the precision of the backtesting engine.

**Why this priority**: Essential for "verification" (matching spreadsheet calculations) and debugging specific trade failures.

**Independent Test**: Checking the generated Trade Log table against the expected signals.

**Acceptance Scenarios**:

1. **Given** multiple trades during a backtest, **When** viewing outcomes, **Then** a sortable table shows Timestamp, Side, Price, and Transaction Fee for each.
2. **Given** the simulation finishes, **When** viewing metrics, **Then** a "Scorecard" displays Sharpe Ratio, Maximum Drawdown, and Total Return.

---

### Edge Cases

- **Empty Results**: What happens if the model generates zero signals for the selected period? (Should show "No Trades Executed" message instead of crashing the charts).
- **Missing Data**: How does the notebook handle date ranges that extend beyond the available CSV data? (Should auto-truncate to data limits and warn the user).
- **GPU/CPU Toggle**: If running in Colab, can the user force CPU mode via the notebook?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a "Configuration" section at the top of the notebook for `SYMBOL`, `START_DATE`, `END_DATE`, `INITIAL_CAPITAL`, and `MODE`.
- **FR-002**: System MUST visualize the combined **Equity Curve** using a line chart.
- **FR-003**: System MUST display an interactive **Signal Overlay** chart (Price vs. Signals).
- **FR-004**: System MUST generate a **Performance Summary** dataframe showing key stats (Sharpe, MaxDD, Win Rate).
- **FR-005**: System MUST allow for **Step-by-Step execution** (Load -> Predict -> Backtest -> Visualize).
- **FR-006**: System MUST support **Google Colab specific visualizations** (ensuring plots render in the Colab output pane).

### Key Entities

- **TestSession**: A container for a specific run instance, holding the configuration and the resulting `BacktestResult`.
- **PlottingEngine**: The abstraction layer (e.g., using `plotly` or `matplotlib`) that converts DataFrames into charts.
- **OutcomeTable**: A formatted view of the trade log and metrics for human reading.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A full "Command Center" run (config to charts) completes in under 15 seconds for 1 year of hourly data.
- **SC-002**: Users can toggle between "Mock" and "Real" modes with exactly ONE variable change in the notebook.
- **SC-003**: Visualization charts are responsive (e.g., zoomable) to allow inspecting individual trade entries.
- **SC-004**: PnL numbers on the chart MUST match the numbers in the summary table within 10 decimal points of precision.
