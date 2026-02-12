# PurePlay Audio

PurePlay Audio is a fully self-contained offline audio processing system that operationalizes an AI-based source separation model (Demucs) into a deterministic Windows standalone executable.

The system embeds its runtime, dependencies, and AI model components, requiring no Python installation, no external services, and no environment configuration.

PurePlay represents a transition from development-stage experimentation to production-style standalone operationalization.

---

## Architectural Overview

PurePlay is structured around four core layers:

### 1. Runtime Resolution Layer
- Detects frozen execution (PyInstaller)
- Dynamically resolves execution paths
- Isolates input/output directories

### 2. AI Operationalization Layer
- Embedded Demucs (htdemucs) model
- CPU execution
- No runtime downloads
- No user-adjustable AI parameters

### 3. Deterministic Assembly Layer
- Predefined audio profiles
- Direct stem recomposition
- Peak normalization (~98%)
- No creative automation

### 4. Distribution Layer
- Packaged using PyInstaller
- Embedded Python runtime
- Embedded Torch and model dependencies
- No modification of host environment
- Fully offline execution

---

## Design Principles

- Fail-fast error handling
- Deterministic and reproducible output
- No silent recovery
- No partial output generation
- No runtime dependency installation
- Strict scope control

---

## Operationalization Strategy

Initial development relied on environment-dependent execution (WSL and manual dependency management).  
To eliminate deployment friction and ensure runtime stability:

- The AI model and runtime were embedded into a single executable
- Environment abstraction was implemented
- Dependency isolation was enforced
- Multi-machine validation was performed

The final result is a portable executable with consistent runtime behavior.

---

## Technical Stack

- Python
- PyTorch
- Demucs
- Torchaudio
- NumPy
- SoundFile
- PyInstaller

---

## Scope

PurePlay v1 is intentionally constrained:

Included:
- AI-based source separation
- Deterministic audio profile generation
- Standalone Windows executable
- Offline processing

Excluded:
- Creative remixing
- Adaptive AI behavior
- Cloud processing
- User configuration layers
- External dependency installation

---

## Version

v1.0 — Stable standalone release

Binary distribution is not publicly available.
