# ez-video-convert
A repo for easily converting videos from one form to another using a command line interface (CLI).

## Installation

```bash
pip install ez-video-convert
```

## Usage

1. Copy the path of the `.mov` file you wish to convert to your clipboard.
2. Open the terminal and simply run

```bash
mov2mp4
```

The script will produce an `.mp4` file in the same location as the `.mov` file.

## Dependencies

- This tool uses `ffmpeg` under the hood, so you will need to have that installed on your system
- The clipboard functionality is provided by `pyperclip`