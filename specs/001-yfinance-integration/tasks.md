# Tasks: yfinance Integration

**Input**: Design documents from `/specs/001-yfinance-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Included as per implementation plan.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- - Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Update `requirements.txt` to include `yfinance` and `pytest`
- [x] T002 Create `tests/` directory structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

*No complex foundational tasks identified. Proceeding to User Stories.*

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Auto-fetch Missing Data (Priority: P1) 🎯 MVP

**Goal**: Automatically fetch and cache OHLCV data from Yahoo Finance when local files are missing.

**Independent Test**: Delete local data for a symbol (e.g., "AAPL") and verify it is re-fetched and saved.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T003 [US1] Create `tests/test_data_loader.py` with mock tests for fetching logic
- [x] T004 [US1] Create manual verification script `verify_yfinance.py` for end-to-end testing

### Implementation for User Story 1

- [x] T005 [US1] Implement `load_ohlcv` fetching and caching logic in `lib/data_loader.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Data Normalization (Priority: P1)

**Goal**: Ensure fetched data matches internal schema (lowercase columns, DatetimeIndex).

**Independent Test**: Verify DataFrame columns are `['open', 'high', 'low', 'close', 'volume']` and index is datetime.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T006 [US2] Update `tests/test_data_loader.py` to test column normalization

### Implementation for User Story 2

- [x] T007 [US2] Implement column normalization and DatetimeIndex enforcement in `lib/data_loader.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T008 Run full verification suite (pytest and manual script)

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

- **User Story 1 (P1)**: Can start after Setup.
- **User Story 2 (P1)**: Can start after Setup. May integrate with US1 logic but can be tested independently.

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority
