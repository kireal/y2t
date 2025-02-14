# YouTube Transcript Extractor (y2t)

A Python tool to extract transcripts from YouTube videos with support for English and Russian languages.

## Installation

This project uses Poetry for dependency management. You have two installation options:

### 1. Global Installation

To install the tool globally and use it from anywhere:

```bash
# Install globally using poetry
poetry build
pip install dist/*.whl
```

Or install directly from the repository:

```bash
pip install git+https://github.com/kireal/y2t.git
```

After global installation, you can use the `y2t` command directly without `poetry run`:

```bash
y2t "https://www.youtube.com/watch?v=jNQXAC9IVRw"
```

### 2. Local Installation

For development or local use:

1. Make sure you have Poetry installed
2. Clone this repository
3. Run:

```bash
poetry install
```

### 3. Uninstallation

To remove the tool:

```bash
# If installed globally with pip
pip uninstall y2t

# If installed locally with poetry
poetry env remove
```

## Usage

The tool can be used in the following ways:

```bash
# With local poetry installation:
poetry run y2t "https://www.youtube.com/watch?v=jNQXAC9IVRw"

# Or if installed globally:
y2t "https://www.youtube.com/watch?v=jNQXAC9IVRw"

# Save transcript to a specific file
y2t -f output.txt "https://www.youtube.com/watch?v=jNQXAC9IVRw"

# Save transcript to a directory (creates file named after video title)
y2t -d transcripts/ "https://www.youtube.com/watch?v=jNQXAC9IVRw"

# Copy transcript to clipboard
y2t -c "https://www.youtube.com/watch?v=jNQXAC9IVRw"
```

The tool supports various YouTube URL formats:

- `youtube.com/watch?v=VIDEO_ID`
- `youtu.be/VIDEO_ID`
- `youtube.com/embed/VIDEO_ID`

## Features

- Extracts transcripts from YouTube videos
- Supports English and Russian languages (prioritizes English)
- Can output to stdout, file, or directory
- When using directory output, saves transcripts as cleaned video titles
- Handles various YouTube URL formats
- Uses TextFormatter for clean transcript output

## Testing

To run tests:

```bash
poetry run pytest
```

## Development

The project structure is organized as follows:

```tree
y2t/
├── y2t/
│   └── __init__.py      # Main implementation
├── tests/
│   ├── conftest.py      # Test fixtures
│   └── test_y2t.py      # Test cases
├── pyproject.toml       # Project configuration and dependencies
└── README.md           # This file
```
