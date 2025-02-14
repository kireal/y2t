# YouTube Transcript Extractor (y2t)

A Python tool to extract transcripts from YouTube videos with support for English and Russian languages.

## Installation

This project uses Poetry for dependency management. You have two installation options:

### 1. Global Installation

To install the tool globally and use it from anywhere:

```bash
# Option 1: Direct installation from repository (recommended)
pip install git+https://github.com/kireal/y2t.git

# Option 2: Build and install from source
poetry build
pip install dist/*.whl
```

If the command is still not found after installation, ensure your Python scripts directory is in your PATH:

For bash/zsh users, add to your `~/.bashrc` or `~/.zshrc`:

```bash
# Add Python scripts directory to PATH
export PATH="$HOME/.local/bin:$PATH"
```

Then reload your shell configuration:

```bash
source ~/.bashrc  # or source ~/.zshrc for zsh users
```

### 2. Alfred Workflow Integration (macOS)

For quick access to transcripts directly from Alfred:

1. Make sure y2t is installed globally (see above)
2. Double-click the `y2t.alfredworkflow` file in the `alfred` folder to install it
   - Or download it from the releases page
   - The workflow will be automatically imported into Alfred

Using the workflow:

1. Open Alfred (default: ⌥ Space)
2. Type `yt` followed by the YouTube URL
3. Press Enter
4. The transcript will be automatically copied to your clipboard

Example:

```alfred
yt https://www.youtube.com/watch?v=jNQXAC9IVRw
```

### 3. Local Installation

For development or local use:

1. Make sure you have Poetry installed
2. Clone this repository
3. Run:

```bash
poetry install
```

### 4. Uninstallation

To remove the tool:

```bash
# If installed globally with pip
pip uninstall y2t

# If installed locally with poetry
poetry env remove

# For Alfred workflow
# Open Alfred Preferences > Workflows and remove the y2t workflow
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

# Using Alfred workflow (automatically copies to clipboard)
# Just type in Alfred:
yt https://www.youtube.com/watch?v=jNQXAC9IVRw
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
- Alfred workflow integration for quick access (macOS)

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
├── alfred/
│   └── y2t.alfredworkflow  # Alfred workflow for quick access
├── pyproject.toml       # Project configuration and dependencies
└── README.md           # This file
```
