# YouTube Transcript Extractor

A Python tool to extract transcripts from YouTube videos with support for English and Russian languages.

## Installation

This project uses Poetry for dependency management. To install:

1. Make sure you have Poetry installed
2. Clone this repository
3. Run:

```bash
poetry install
```

## Usage

The script can be run in two ways:

1. Output transcript to stdout:

```bash
poetry run python youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

1. Save transcript to a file:

```bash
poetry run python youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID" -f output.txt
```

The script supports various YouTube URL formats:

- `youtube.com/watch?v=VIDEO_ID`
- `youtu.be/VIDEO_ID`
- `youtube.com/embed/VIDEO_ID`

## Features

- Extracts transcripts from YouTube videos
- Supports English and Russian languages (prioritizes English)
- Can output to stdout or file
- Handles various YouTube URL formats
- Uses TextFormatter for clean transcript output
  