#!/usr/bin/env python3

import argparse
import re
import os
from typing import Optional, Tuple
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import pyperclip
import requests


def clean_filename(title: str) -> str:
    """Clean up video title for use as filename."""
    # Trim leading/trailing spaces first
    title = title.strip()
    # Replace spaces with underscores
    title = re.sub(r"\s+", "_", title)
    # Remove special characters
    title = re.sub(r"[^\w\-_.]", "", title)
    return title


def get_video_info(video_id: str) -> Tuple[str, str]:
    """Get video title and cleaned filename from YouTube."""
    try:
        # Use YouTube's oEmbed endpoint to get video information
        response = requests.get(
            f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={video_id}&format=json"
        )
        response.raise_for_status()
        title = response.json()["title"]
        filename = clean_filename(title)
        return title, filename
    except Exception as e:
        raise ValueError(f"Failed to get video title: {str(e)}")


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
    video_id: str,
    output_file: Optional[str] = None,
    output_dir: Optional[str] = None,
    copy_to_clipboard: bool = False,
) -> None:
    """
    Get transcript for a YouTube video and output it to stdout or file.

    Args:
        video_id: YouTube video ID
        output_file: Optional specific output file path
        output_dir: Optional directory to save transcript with video title as filename
        copy_to_clipboard: Whether to copy transcript to clipboard
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(["en", "ru"])
        formatter = TextFormatter()

        formatted_transcript = formatter.format_transcript(transcript.fetch())

        if output_dir:
            # Get video title and create filename
            _, filename = get_video_info(video_id)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{filename}.txt")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(formatted_transcript)
            print(f"Transcript has been saved to {output_path}")
        elif output_file:
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
        "-d",
        "--dir",
        help="Output directory (transcript will be saved as video_title.txt)",
    )
    parser.add_argument(
        "-c", "--clipboard", action="store_true", help="Copy transcript to clipboard"
    )

    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.url)
        get_transcript(video_id, args.file, args.dir, args.clipboard)
    except ValueError as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
