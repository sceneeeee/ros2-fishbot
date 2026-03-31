import rclpy
from rclpy.node import Node
from autopatrol_interfaces.srv import SpeechText
import espeakng

class Speaker(Node):
    def __init__(self):
        super().__init__('speaker')
        self.speech_service_ = self.create_service(SpeechText, 'speech_text', self.speech_text_callback)
        self.get_logger().info('Speaker node has been started.')
        self.speaker_ = espeakng.Speaker()
        self.speaker_.voice = ('zh')

    def speech_text_callback(self, request, response):
        text = request.text
        self.get_logger().info(f'Received text to speak: "{text}"')

        self.speaker_.say(text)
        self.speaker_.wait()

        
        response.result = True
        return response
    
def main():
    rclpy.init()
    node = Speaker()
    rclpy.spin(node)
    rclpy.shutdown()