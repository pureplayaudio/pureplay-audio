# Architecture

PurePlay v1 is designed as a self-contained AI operationalization system.

## Architectural Layers

### 1. Runtime Resolution Layer

- Detects frozen execution (PyInstaller)
- Resolves base directory dynamically
- Manages internal `/input` and `/output` folders

### 2. AI Operationalization Layer

- Embedded Demucs model (htdemucs)
- CPU execution
- Fixed configuration
- No user-adjustable parameters

The AI layer is responsible only for source separation.

### 3. Deterministic Assembly Layer

- Predefined musical profiles
- Direct summation of selected stems
- Peak normalization (~98%)
- No creative processing

### 4. Distribution Layer

- Packaged using PyInstaller
- Embedded Python runtime
- Embedded Torch and Demucs dependencies
- No installation on host system
- No environment modification

## Determinism

Given:
- Same input audio
- Same profile
- Same executable version

The output is reproducible.

No adaptive logic is applied.