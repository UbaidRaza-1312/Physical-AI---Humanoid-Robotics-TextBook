import requests
import json
import os

# Placeholder for actual audio recording and OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WHISPER_API_URL = "https://api.openai.com/v1/audio/transcriptions"

def transcribe_audio(audio_file_path):
    """
    Transcribes an audio file using the OpenAI Whisper API.

    Args:
        audio_file_path (str): Path to the audio file (e.g., .wav, .mp3).

    Returns:
        str: Transcribed text, or None if an error occurred.
    """
    if not os.path.exists(audio_file_path):
        print(f"Error: Audio file not found at {audio_file_path}")
        return None

    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return None

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    with open(audio_file_path, "rb") as audio_file:
        files = {
            "file": audio_file,
            "model": (None, "whisper-1")
        }
        # Optional parameters can be added here, e.g., "language": (None, "en")
        # data = {"model": "whisper-1", "language": "en"}

        try:
            response = requests.post(WHISPER_API_URL, headers=headers, files=files)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

            transcription = response.json()
            return transcription.get("text")

        except requests.exceptions.RequestException as e:
            print(f"API Request failed: {e}")
            if response is not None:
                print(f"Response status: {response.status_code}")
                print(f"Response content: {response.text}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON response: {response.text}")
            return None

def record_audio_placeholder(output_filename="recorded_command.wav", duration_seconds=5):
    """
    Placeholder function for recording audio.
    In a real implementation, this would use an audio library (e.g., sounddevice, pyaudio).
    """
    print(f"Simulating audio recording for {duration_seconds} seconds into {output_filename}...")
    # This would actually record audio. For demonstration, we'll just create a dummy file.
    with open(output_filename, "w") as f:
        f.write("This is a dummy audio file content.")
    print("Dummy audio file created.")
    return output_filename

if __name__ == "__main__":
    # Example usage:
    # 1. Simulate recording a voice command
    recorded_file = record_audio_placeholder()

    # 2. Transcribe the recorded audio
    if recorded_file:
        print(f"\nTranscribing audio file: {recorded_file}")
        transcribed_text = transcribe_audio(recorded_file)

        if transcribed_text:
            print(f"\nTranscribed Text: \"{transcribed_text}\"")
        else:
            print("\nFailed to transcribe audio.")
    
    # Clean up dummy file
    if os.path.exists(recorded_file):
        os.remove(recorded_file)
