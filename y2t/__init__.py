#!/usr/bin/env python3

import argparse
import re
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import pyperclip


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL."""
    # Regular expression pattern for YouTube URLs
    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube URL")


def get_transcript(
    video_id: str, output_file: Optional[str] = None, copy_to_clipboard: bool = False
) -> None:
    """Get transcript for a YouTube video and output it to stdout or file."""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(["en", "ru"])
        formatter = TextFormatter()

        formatted_transcript = formatter.format_transcript(transcript.fetch())

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(formatted_transcript)
            print(f"Transcript has been saved to {output_file}")
        else:
            print(formatted_transcript)

        if copy_to_clipboard:
            pyperclip.copy(formatted_transcript)
            print("\nTranscript has been copied to clipboard!")

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube video transcripts")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-f", "--file", help="Output file path (optional)")
    parser.add_argument(
        "-c", "--clipboard", action="store_true", help="Copy transcript to clipboard"
    )

    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.url)
        get_transcript(video_id, args.file, args.clipboard)
    except ValueError as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
