# Tasks: Test Command Center

**Input**: Design documents from `/specs/004-test-command-center/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Test tasks are included to verify charting logic and metric calculations as per the verification plan.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 [P] Ensure `plotly` and `ipywidgets` are in `requirements.txt`
- [x] T002 [P] Create `lib/visualizer.py` skeleton
- [x] T003 [P] Create `tests/test_visualizer.py` skeleton
- [x] T004 Create `notebooks/Test_Command_Center.ipynb` initial structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Implement `ExperimentLogger` in `lib/reporting.py` for JSON logging to `results/`
- [x] T006 [P] Implement base `TestSession` entity in `lib/visualizer.py` as per `data-model.md`
- [x] T007 Implement helper to load data from `data/*.csv` with date filtering in `lib/data_loader.py` (if not existing)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 2 - Parametric Test Control (Priority: P1) 🎯 MVP Component

**Goal**: Researcher can define test constraints in the notebook UI.

**Independent Test**: Change a variable in the notebook cockpit and verify the system's `BacktestConfig` updates.

### Implementation for User Story 2

- [x] T008 [US2] Implement `ipywidgets` cockpit (Symbol Dropdown, Mode Toggle, DateRangeSlider, Run Button) in `notebooks/Test_Command_Center.ipynb`
- [x] T009 [US2] Implement `BacktestConfig` parsing logic to interface with `StrategyFactory` with "Small Data" defaults (last 500 bars)
- [x] T010 [US3] (Early implementation) Add "Threshold" and "Initial Capital" widgets to cockpit

**Checkpoint**: Parametric controls are functional and can trigger baseline backtest logic.

---

## Phase 4: User Story 1 - Interactive Visualization (Priority: P1) 🎯 MVP Component

**Goal**: Visualize backtest results graphically (Equity Curve, Drawdowns, Signals).

**Independent Test**: Run a backtest then call the plotting function; confirm interactive Plotly charts appear.

### Tests for User Story 1

- [ ] T011 [P] [US1] Create test in `tests/test_visualizer.py` to verify data merging for Plotly traces using 100-bar sample data

### Implementation for User Story 1

- [ ] T012 [P] [US1] Implement `plot_equity_curve` in `lib/visualizer.py` (Strategy vs Buy & Hold)
- [ ] T013 [P] [US1] Implement `plot_signals` in `lib/visualizer.py` (Price candles with Signal markers)
- [ ] T014 [US1] Integrate `plotly` rendering cells in `notebooks/Test_Command_Center.ipynb`
- [ ] T015 [US1] Ensure Plotly responsive layout for mobile/Colab viewing

**Checkpoint**: Visualizations are live and interactive in the notebook.

---

## Phase 5: User Story 3 - Outcome Audit Tables (Priority: P2)

**Goal**: Detailed trade tables and performance scorecard for precision verification.

**Independent Test**: View the "Audit" section of the notebook and match table entries to the chart's signal markers.

### Implementation for User Story 3

- [x] T016 [P] [US3] Implement `PerformanceScorecard` renderer in `lib/visualizer.py` using Pandas Styler for premium look
- [x] T017 [P] [US3] Implement `TradeLogTable` renderer in `lib/visualizer.py` with sortable columns
- [x] T018 [US3] Update `notebooks/Test_Command_Center.ipynb` to display scorecard and trade logs after backtest

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T019 [P] Update `specs/004-test-command-center/quickstart.md` with final screenshots or usage tips
- [x] T020 [P] Run final validation of the notebook using "Real" mode on small data (CPU-friendly)
- [x] T021 Code cleanup and refactoring of `lib/visualizer.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup.
- **User Stories (Phase 3 & 4)**: Priority P1, can run in parallel after Foundation.
- **User Story (Phase 5)**: Priority P2, depends on Phase 4 visualizations for context.

### Parallel Opportunities

- T001, T002, T003 (Setup)
- T012, T013 (Visualization logic)
- T016, T017 (Audit UI)

---

## Implementation Strategy

### MVP First (User Story 1 & 2)
Focus on getting the "Parameters -> Run -> Charts" loop working first. This delivers the core value.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Verify charts render in Colab (interactive mode)
- **Constraint**: All local tests and default notebook runs MUST use < 500 rows for CPU efficiency.
