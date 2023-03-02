import rclpy
from rclpy.node import Node
import board
import adafruit_bmp3xx
from adafruit_bmp3xx import PowerMode, ODRMode
import digitalio
import enum
from std_msgs.msg import Float64MultiArray    

class MinimalPublisher(Node):

    def __init__(self, bmp):
        super().__init__('sensor_pub')
        self.publisher_ = self.create_publisher(Float64MultiArray, 'sensor_topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.bmp = bmp

    def timer_callback(self):
        array = [self.bmp.pressure,self.bmp.temperature]
        msg = Float64MultiArray(data=array)
        self.publisher_.publish(msg)

def main(args=None):

    spi = board.SPI()
    cs = digitalio.DigitalInOut(board.D7)
    bmp = adafruit_bmp3xx.BMP3XX_SPI(spi, cs)
    bmp.sea_level_pressure = 1013.25

    bmp.pressure_oversampling = 8
    bmp.temperature_oversampling = 4
    bmp.filter_coefficient = 2

    ODR = ODRMode.ODR_25
    bmp.output_data_rate = ODR

    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher(bmp)

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()