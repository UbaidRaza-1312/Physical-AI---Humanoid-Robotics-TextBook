# API Contract: OpenAI Whisper for Speech-to-Text

## Description
This contract outlines the expected interaction with the OpenAI Whisper API for converting spoken language into text. This is crucial for the Vision-Language-Action (VLA) module in the textbook's capstone project, enabling the humanoid robot to understand voice commands.

## Endpoint
- **URL**: `https://api.openai.com/v1/audio/transcriptions`
- **Method**: `POST`

## Request
- **Header**:
    - `Authorization`: `Bearer YOUR_API_KEY`
    - `Content-Type`: `multipart/form-data`
- **Body (multipart/form-data)**:
    - `file`: (Required) The audio file to transcribe. Must be one of `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `wav`, `webm`.
    - `model`: (Required) ID of the model to use. Currently, only `whisper-1` is supported.
    - `language`: (Optional) The language of the input audio. Supplying the input language in ISO-639-1 format improves accuracy and latency.
    - `prompt`: (Optional) An optional text to guide the model's style or continue a previous audio segment.
    - `response_format`: (Optional) The format of the transcript output, one of `json`, `text`, `srt`, `verbose_json`, or `vtt`. Defaults to `json`.
    - `temperature`: (Optional) Controls creativity. Higher values (up to 1.0) increase randomness; lower values (down to 0.0) make it more deterministic. Defaults to `0.0`.

## Response (Success: 200 OK)
- **Content-Type**: `application/json` (if `response_format` is `json` or `verbose_json`)
- **Body (Example for `json` format)**:
```json
{
  "text": "This is a transcript of the audio input."
}
```

## Response (Error)
- **Status Codes**:
    - `400 Bad Request`: Invalid input or parameters.
    - `401 Unauthorized`: Missing or invalid API key.
    - `429 Too Many Requests`: Rate limit exceeded.
    - `500 Internal Server Error`: OpenAI server issue.
- **Body (Example)**:
```json
{
  "error": {
    "message": "Error message details.",
    "type": "invalid_request_error",
    "param": null,
    "code": null
  }
}
```

## Versioning Strategy
- OpenAI API typically handles versioning internally. Developers should follow official OpenAI documentation for updates.

## Idempotency, Timeouts, Retries
- **Idempotency**: Not inherently idempotent for transcription; each request processes new audio.
- **Timeouts**: Client-side timeouts should be implemented to prevent indefinite waits.
- **Retries**: Exponential backoff with jitter should be used for transient errors (`429`, `500` series).

## Error Taxonomy
- `INVALID_AUDIO_FORMAT`: Provided audio file is not supported.
- `MISSING_API_KEY`: Authentication token is not provided.
- `RATE_LIMIT_EXCEEDED`: Too many requests in a given period.
- `SERVICE_UNAVAILABLE`: Temporary issue with the OpenAI service.
