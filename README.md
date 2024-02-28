# ConvertLite

ConvertLite is a versatile file conversion tool built with Python and PyQt5, supporting image, video, and document formats. It offers a simple drag-and-drop interface for easy file conversion. Logo generated using AI (Bing in the 24th Februrary 2024 - 21:16).

## Features

- **Image Conversion**: Supports formats like PNG, JPG, JPEG, GIF, BMP, and SVG.
- **Video Conversion**: Supports MP4, MOV, MKV formats.
- **Document Conversion**: Support for PDF format.

- Click or drag a file into the program
- Select which type you want to convert it in or shift+click to also adjust image/video settings
- Get the converted file in the same directory as the old one
## Installation

### Prerequisites

- Python 3.6 or newer.
- `ffmpeg` for video processing.

### Setup

1. **Clone the repository**:

```bash
git clone https://github.com/TRC-Loop/ConvertLite.git
cd ConvertLite
```

2. **Install Python Dependencies**:

Without a virtual environment:

```bash
pip install -r requirements.txt
```

Or with a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. **Install ffmpeg**:

- **macOS**:
  
  ```bash
  brew install ffmpeg
  ```

- **Linux**:
  
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

- **Windows**:

  Download and install `ffmpeg` from [ffmpeg.org](https://ffmpeg.org/download.html). Add the path to the `ffmpeg` binary to your system's PATH variable.

## Usage

To start ConvertLite, navigate to the project directory and run:

```bash
python main.py
```

## Troubleshooting

### ffmpeg not found

If you encounter an error stating that `ffmpeg` could not be found, ensure that `ffmpeg` is correctly installed and its path is added to your system's PATH environment variable. Alternatively, you can set the `IMAGEIO_FFMPEG_EXE` environment variable to the path of the `ffmpeg` executable.

#### Setting the `IMAGEIO_FFMPEG_EXE` variable:

- **macOS/Linux**:

  ```bash
  export IMAGEIO_FFMPEG_EXE=/path/to/ffmpeg
  ```

- **Windows**:

  ```cmd
  set IMAGEIO_FFMPEG_EXE=C:\path\to\ffmpeg.exe
  ```

### Python Package Issues

If you face issues with Python packages, ensure you have the correct version of Python installed and you are using the correct pip version (`pip`, `pip3`, or specifying with `python -m pip`). Reinstall the dependencies ensuring no errors are encountered during the installation.
