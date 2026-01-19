# Tasks: Model Integration

**Feature Branch**: `003-model-integration`
**Status**: In Progress

## Dependencies

- Phase 1: Setup (Setup) -> Phase 2: User Story 1 (Local Inference) -> Phase 3: User Story 2 (Colab Support) -> Phase 4: User Story 3 (Strategy Integration) -> Phase 5: Polish & Verify

## Phase 1: Setup

**Goal**: Prepare environment for PyTorch and Model loading.

- [ ] T001 Update `requirements.txt` with `torch`, `transformers`
- [ ] T002 Create `tests/test_kronos_model.py` skeleton
- [ ] T003 Create `tests/test_factory.py` skeleton

## Phase 2: User Story 1 - Local Inference Pipeline (Priority: P1)

**Goal**: Model loads and runs locally on CPU/MPS.
**Independent Test**: `pytest tests/test_kronos_model.py` verifies model instantiation and signal generation.

- [ ] T004 [US1] Create `lib/kronos_model.py` with `KronosModel` class structure
- [ ] T005 [US1] Implement environment detection (Colab vs Local) in `lib/kronos_model.py`
- [ ] T006 [US1] Implement dynamic import of `Kronos` repo in `lib/kronos_model.py`
- [ ] T007 [US1] Implement `generate_signals` in `KronosModel` using actual `KronosPredictor`
- [ ] T008 [US1] Implement unit tests for `KronosModel` in `tests/test_kronos_model.py` (mocking the external repo)
- [ ] T009 [US1] Verify local inference manually using `verify_quickstart.py` (modified)

## Phase 3: User Story 2 - Google Colab Support (Priority: P1)

**Goal**: Codebase works in Colab environment (Linux/CUDA).
**Independent Test**: Colab notebook runs successfully.

- [ ] T010 [US2] Update `lib/kronos_model.py` to confirm CUDA usage when available
- [ ] T011 [US2] Create Colab-friendly notebook `notebooks/Model_Integration_Test.ipynb`
- [ ] T012 [US2] Document Colab usage instructions in `quickstart.md` details

## Phase 4: User Story 3 - Strategy Integration (Priority: P2)

**Goal**: Switch between Mock and Real strategies via config.
**Independent Test**: `pytest tests/test_factory.py` verifies correct class returned.

- [ ] T013 [US3] Create `lib/strategy_factory.py` with `StrategyFactory` class
- [ ] T014 [US3] Implement `StrategyFactory.create` logic (Real vs Mock)
- [ ] T015 [US3] Refactor `lib/strategy.py` to allow being instantiated/wrapped or used as base
- [ ] T016 [US3] Implement tests for factory in `tests/test_factory.py`
- [ ] T017 [US3] Update `verify_quickstart.py` to use `StrategyFactory`

## Phase 5: Polish & Verify

**Goal**: Final clean up and full regression test.

- [ ] T018 Run full test suite `pytest tests/`
- [ ] T019 Ensure `quickstart.md` is accurate and examples run
