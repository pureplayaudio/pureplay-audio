# Build Instructions

PurePlay is packaged as a standalone Windows executable using PyInstaller.

## Requirements

- Python 3.x
- Torch
- Demucs
- soundfile
- numpy
- torchaudio
- PyInstaller

## Build Command

Example:

pyinstaller pureplay.spec

## Notes

- The executable embeds Python runtime.
- Torch and Demucs dependencies must be properly included in the spec file.
- Ensure model weights are accessible at runtime.
- Build must be tested on clean Windows environment.

## Distribution

The distributed executable:

- Requires no Python installation
- Requires no additional dependencies
- Runs entirely offline