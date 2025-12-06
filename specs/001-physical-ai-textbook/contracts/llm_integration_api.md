# API Contract: LLM Integration (e.g., GPT Models) for Cognitive Planning

## Description
This contract defines the interaction with Large Language Models (LLMs), such as OpenAI's GPT models, for cognitive planning in robotics. This integration enables the humanoid robot to interpret complex natural language commands and translate them into a sequence of actionable robotic tasks (e.g., navigation, object identification, manipulation).

## Endpoint (Example: OpenAI Chat Completions API)
- **URL**: `https://api.openai.com/v1/chat/completions`
- **Method**: `POST`

## Request
- **Header**:
    - `Authorization`: `Bearer YOUR_API_KEY`
    - `Content-Type`: `application/json`
- **Body (Example)**:
```json
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "system",
      "content": "You are a robotic task planner. Convert user commands into a JSON array of discrete robot actions. Actions include: NAVIGATE(location), IDENTIFY(object), GRASP(object), RELEASE(object). Provide only the JSON array."
    },
    {
      "role": "user",
      "content": "Navigate to the kitchen, find the red apple, and pick it up."
    }
  ],
  "temperature": 0.2,
  "max_tokens": 150
}
```
- **Key Parameters**:
    - `model`: (Required) The ID of the model to use.
    - `messages`: (Required) An array of message objects, where each object has a `role` (system, user, assistant) and `content`.
    - `temperature`: (Optional) Sampling temperature, between 0 and 2. Higher values mean the model will take more risks. Defaults to 1.
    - `max_tokens`: (Optional) The maximum number of tokens to generate in the chat completion.

## Response (Success: 200 OK)
- **Content-Type**: `application/json`
- **Body (Example)**:
```json
{
  "id": "chatcmpl-விட்டது",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-4o",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "[
  {\"action\": \"NAVIGATE\", \"target\": \"kitchen\"},
  {\"action\": \"IDENTIFY\", \"object\": \"red apple\"},
  {\"action\": \"GRASP\", \"object\": \"red apple\"}
]"
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 40,
    "total_tokens": 90
  }
}
```
- **Expected `message.content` Format**: A JSON array of robotic actions, each with an `action` type and relevant parameters.

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
- OpenAI API versioning is typically handled internally. Adherence to official OpenAI documentation is required.

## Idempotency, Timeouts, Retries
- **Idempotency**: Requests are not inherently idempotent; each request generates a new completion.
- **Timeouts**: Implement client-side timeouts.
- **Retries**: Employ exponential backoff with jitter for transient errors (`429`, `500` series).

## Error Taxonomy
- `INVALID_INPUT`: Malformed messages array or invalid parameters.
- `MISSING_API_KEY`: Authentication token not provided.
- `RATE_LIMIT_EXCEEDED`: Too many requests in a given period.
- `CONTEXT_LENGTH_EXCEEDED`: Input prompt exceeds the model's maximum context window.
- `SERVICE_UNAVAILABLE`: Temporary issue with the LLM service.
