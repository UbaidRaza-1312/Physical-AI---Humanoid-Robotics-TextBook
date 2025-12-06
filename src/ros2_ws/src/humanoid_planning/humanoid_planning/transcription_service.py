import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from humanoid_interfaces.srv import Transcribe
# from openai import OpenAI # Assuming OpenAI Python client library is installed
# import base64 # For encoding/decoding audio data if needed


class TranscriptionService(Node):
    def __init__(self):
        super().__init__('transcription_service')
        self.get_logger().info('Transcription Service Node started.')

        # TODO: Initialize OpenAI client (API key management, etc.)
        # self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        self.service = self.create_service(
            Transcribe,
            'transcribe_audio',
            self.transcribe_callback,
            callback_group=ReentrantCallbackGroup() # Use reentrant for external API call
        )
        self.get_logger().info('Transcribe service is ready.')

    async def transcribe_callback(self, request, response):
        self.get_logger().info(f'Received transcription request. Audio encoding: {request.encoding}')

        try:
            # TODO: Convert audio_data from byte array to a format Whisper API expects (e.g., file-like object)
            # Example (requires further implementation based on audio source and format):
            # audio_file = io.BytesIO(request.audio_data.tobytes())
            # audio_file.name = "audio.wav" # Whisper API might expect a filename

            # Placeholder for actual API call
            # transcript = await self.openai_client.audio.transcriptions.create(
            #     model="whisper-1",
            #     file=audio_file
            # )
            # response.transcribed_text = transcript.text

            # Mock response for testing without API call
            mock_text = "This is a mock transcription of the audio."
            response.transcribed_text = mock_text
            response.success = True
            response.error_message = ""
            self.get_logger().info(f'Mock transcription result: {mock_text}')

        except Exception as e:
            self.get_logger().error(f'Transcription failed: {e}')
            response.transcribed_text = ""
            response.success = False
            response.error_message = str(e)

        return response

def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor()
    transcription_service = TranscriptionService()
    executor.add_node(transcription_service)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        transcription_service.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
