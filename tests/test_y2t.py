import pytest
from y2t import extract_video_id, get_transcript, clean_filename, get_video_info
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter


def test_clean_filename():
    """Test filename cleaning function."""
    test_cases = [
        ("My Video Title!", "My_Video_Title"),
        ("Video with spaces", "Video_with_spaces"),
        ("Special@#$%^&*Characters", "SpecialCharacters"),
        ("Mixed-Case_Title 123", "Mixed-Case_Title_123"),
        ("   Multiple   Spaces   ", "Multiple_Spaces"),
    ]

    for input_title, expected in test_cases:
        assert clean_filename(input_title) == expected


def test_get_video_info_success(mocker):
    """Test successful video info retrieval."""
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"title": "Test Video Title"}
    mock_response.raise_for_status = mocker.Mock()

    mocker.patch("requests.get", return_value=mock_response)

    title, filename = get_video_info("test_video_id")
    assert title == "Test Video Title"
    assert filename == "Test_Video_Title"


def test_get_video_info_failure(mocker):
    """Test video info retrieval failure."""
    mocker.patch("requests.get", side_effect=Exception("Network error"))

    with pytest.raises(ValueError, match="Failed to get video title"):
        get_video_info("test_video_id")


def test_extract_video_id_valid_urls():
    """Test video ID extraction from various valid YouTube URL formats."""
    test_cases = [
        ("https://www.youtube.com/watch?v=jNQXAC9IVRw", "jNQXAC9IVRw"),
        ("https://youtu.be/jNQXAC9IVRw", "jNQXAC9IVRw"),
        ("https://www.youtube.com/embed/jNQXAC9IVRw", "jNQXAC9IVRw"),
    ]

    for url, expected_id in test_cases:
        assert extract_video_id(url) == expected_id


def test_extract_video_id_invalid_url():
    """Test video ID extraction with invalid URL."""
    with pytest.raises(ValueError, match="Invalid YouTube URL"):
        extract_video_id("https://invalid-url.com")


def test_get_transcript_success(mocker):
    """Test successful transcript retrieval."""
    # Mock data
    mock_transcript_data = [
        {"text": "All right, so here we are at the zoo.", "start": 0.0, "duration": 2.0}
    ]

    # Mock YouTubeTranscriptApi
    mock_transcript = mocker.Mock()
    mock_transcript.fetch.return_value = mock_transcript_data

    mock_transcript_list = mocker.Mock()
    mock_transcript_list.find_transcript.return_value = mock_transcript

    mocker.patch.object(
        YouTubeTranscriptApi, "list_transcripts", return_value=mock_transcript_list
    )

    # Test without file output
    get_transcript("jNQXAC9IVRw")

    # Verify the transcript was requested
    YouTubeTranscriptApi.list_transcripts.assert_called_once_with("jNQXAC9IVRw")
    mock_transcript_list.find_transcript.assert_called_once_with(["en", "ru"])


def test_get_transcript_with_file(mocker, tmp_path):
    """Test transcript retrieval with file output."""
    # Mock data
    mock_transcript_data = [
        {"text": "All right, so here we are at the zoo.", "start": 0.0, "duration": 2.0}
    ]

    # Mock YouTubeTranscriptApi
    mock_transcript = mocker.Mock()
    mock_transcript.fetch.return_value = mock_transcript_data

    mock_transcript_list = mocker.Mock()
    mock_transcript_list.find_transcript.return_value = mock_transcript

    mocker.patch.object(
        YouTubeTranscriptApi, "list_transcripts", return_value=mock_transcript_list
    )

    # Create temporary file path
    output_file = tmp_path / "transcript.txt"

    # Test with file output
    get_transcript("jNQXAC9IVRw", str(output_file))

    # Verify file was created and contains content
    assert output_file.exists()
    assert output_file.read_text()


def test_get_transcript_with_directory(mocker, tmp_path):
    """Test transcript retrieval with directory output."""
    # Mock transcript data
    mock_transcript_data = [
        {"text": "All right, so here we are at the zoo.", "start": 0.0, "duration": 2.0}
    ]

    # Mock YouTubeTranscriptApi
    mock_transcript = mocker.Mock()
    mock_transcript.fetch.return_value = mock_transcript_data

    mock_transcript_list = mocker.Mock()
    mock_transcript_list.find_transcript.return_value = mock_transcript

    mocker.patch.object(
        YouTubeTranscriptApi, "list_transcripts", return_value=mock_transcript_list
    )

    # Mock video info
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"title": "Test Video Title"}
    mock_response.raise_for_status = mocker.Mock()
    mocker.patch("requests.get", return_value=mock_response)

    # Test with directory output
    output_dir = tmp_path / "transcripts"
    get_transcript("test_video_id", output_dir=str(output_dir))

    # Verify file was created with correct name and contains content
    expected_file = output_dir / "Test_Video_Title.txt"
    assert expected_file.exists()
    assert expected_file.read_text()


def test_get_transcript_no_captions(mocker):
    """Test transcript retrieval when captions are disabled."""
    mocker.patch.object(
        YouTubeTranscriptApi,
        "list_transcripts",
        side_effect=TranscriptsDisabled("Transcripts are disabled for this video"),
    )

    with pytest.raises(SystemExit) as exc_info:
        get_transcript("jNQXAC9IVRw")
    assert exc_info.value.code == 1


if __name__ == "__main__":
    pytest.main()
