import rclpy
from rclpy.node import Node

from radar_msgs.msg import RadarTracks
from geometry_msgs.msg import PoseArray, Pose


class RADAR_sub(Node):

    def __init__(self):
        super().__init__('RADAR_sub')
        self.subscription = self.create_subscription(RadarTracks,'/objects',self.listener_callback,10)
        self.subscription  # prevent unused variable warning
        self.publisher = self.create_publisher(PoseArray, '/object/points', 10)

    def listener_callback(self, msg):
        poses_msg = PoseArray()
        n = len(msg.tracks)
        objs = msg.tracks
        for i in objs:
            p = Pose()
            p.position = i.position
            poses_msg.poses.append(p)
    
        poses_msg.header.stamp = self.get_clock().now().to_msg()
        poses_msg.header.frame_id = 'velodyne32'
        self.get_logger().info(f'{n}')
        self.publisher.publish(poses_msg)

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = RADAR_sub()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
