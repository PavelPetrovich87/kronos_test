# Research: Model Integration

**Status**: In Progress
**Decision**: Dynamic Environment Detection + Configurable Paths

## Decisions

### 1. Environment Detection (Colab vs Local)

- **Problem**: File paths and GPU availability differ between Local (Mac) and Colab (Linux/Cloud).
- **Decision**: Use `sys.modules` check for `google.colab` to detect environment.
- **Implementation**:
    - If Colab: Base path defaults to `/content/Kronos`.
    - If Local: Base path defaults to `../Kronos` (or configured path).
- **Rationale**: Robust and standard way to detect Colab runtime.

### 2. Model Loading & Dependency handling

- **Problem**: `Kronos` is a separate repo.
- **Decision**: Assume `Kronos` is cloned alongside `kronos_test` (Local) or inside workspace (Colab).
- **Fallback**: Allow `KRONOS_PATH` env var or config override.
- **Rationale**: Flexible for different dev setups.

### 3. Strategy Switcher

- **Problem**: Need to alternate between Real and Mock models.
- **Decision**: Factory pattern in `lib/strategy.py` or new `lib/factory.py`.
- **Implementation**: `StrategyFactory.create(config)` returns either `KronosStrategy` (real) or `MockStrategy`.
- **Rationale**: Separation of concerns.

### 4. GPU/CPU Logic

- **Decision**: Use `torch.device("cuda" if torch.cuda.is_available() else "cpu")`.
- **Mac Support**: Add check for `mps` (Metal Performance Shaders) for Mac users?
    - *Research*: PyTorch on Mac uses `mps`.
    - *Refinement*: `device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"`
### 5. Inference Execution (Constraint)

- **Context**: Kronos has no external inference API/provider.
- **Decision**: All inference must be **Embedded/In-Process**.
- **Implication**:
    - **Computex Requirements**: The runtime (Local Mac or Colab VM) MUST have sufficient RAM/VRAM to hold the model.
    - **No API Fallback**: We cannot offload heavy compute to a remote service.
    - **Colab**: The Notebook runtime itself IS the inference server.

