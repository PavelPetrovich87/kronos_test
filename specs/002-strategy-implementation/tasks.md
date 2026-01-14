# Tasks: Strategy Implementation

**Input**: Design documents from `/specs/002-strategy-implementation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Included as per implementation plan.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- - Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create `specs/002-strategy-implementation/tasks.md` (this file)
- [x] T002 Update `lib/reporting.py` with empty class structure
- [x] T003 Update `lib/strategy.py` with empty class structure
- [x] T004 Update `lib/backtester.py` with modified structure from research
- [x] T005 [P] Create `tests/test_strategy.py` skeleton
- [x] T006 [P] Create `tests/test_backtester.py` skeleton
- [x] T007 [P] Create `tests/test_risk.py` skeleton

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T008 Implement `lib/reporting.py` (Sharpe, Max Drawdown calculations)
- [x] T009 Implement `Signal`, `Trade`, `BacktestResult` data classes in `lib/strategy.py` (or shared model file if preferred)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Signal Generation (Priority: P1) 🎯 MVP

**Goal**: Convert raw predictions into Long/Short/Neutral signals.

**Independent Test**: Feed mock predictions to `Strategy.generate_signals` and verify correct Enum output.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T010 [US1] Implement unit tests for signal logic in `tests/test_strategy.py`

### Implementation for User Story 1

- [x] T011 [US1] Implement `Strategy.generate_signals` logic in `lib/strategy.py`
- [x] T012 [US1] Add signal threshold configuration handling

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Backtesting Engine (Priority: P1)

**Goal**: Simulate trades and calculate PnL based on signals.

**Independent Test**: Run a backtest on known data and signals, verifying equity matches expected list.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T013 [US2] Implement integration tests in `tests/test_backtester.py`

### Implementation for User Story 2

- [x] T014 [US2] Implement `Backtester.run` loop in `lib/backtester.py`
- [x] T015 [US2] Implement transaction cost logic in `lib/backtester.py`
- [x] T016 [US2] Implement equity curve calculation in `lib/backtester.py` (using `reporting.py`)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Risk Management (Priority: P2)

**Goal**: Filter trades during high volatility.

**Independent Test**: Verify trades are rejected when volatility exceeds threshold.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T017 [US3] Implement risk tests in `tests/test_risk.py`

### Implementation for User Story 3

- [x] T018 [US3] Implement `RiskManager` class in `lib/risk.py`
- [x] T019 [US3] Integrate `RiskManager` into `Backtester` loop in `lib/backtester.py`

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T020 Verify `quickstart.md` examples run correctly
- [x] T021 Run full test suite `pytest tests/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational.
- **User Story 2 (P1)**: Can start after Foundational.
- **User Story 3 (P2)**: Best done after Backtester (US2) is basic working.

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority
