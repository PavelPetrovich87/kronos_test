# Data Model: Model Integration

## Entities

### `ModelConfig`
Configuration object passed to `KronosModel`.

| Field | Type | Description |
|-------|------|-------------|
| `model_name` | `str` | HuggingFace model ID or local path |
| `tokenizer_name` | `str` | HuggingFace tokenizer ID |
| `device` | `str` | Execution device: 'cuda', 'mps', 'cpu' |
| `max_context` | `int` | Maximum sequence length (e.g., 512) |
| `top_p` | `float` | Nucleus sampling parameter |
| `temperature` | `float` | Sampling temperature |
| `sample_count` | `int` | Number of samples to generate |

### `Prediction`
Represents the raw output from the model before conversion to Signal.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `datetime` | Time of prediction |
| `predicted_close` | `float` | Forecasted close price |
| `confidence` | `float` | Optional confidence score (if available) |
