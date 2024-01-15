import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseArray, Pose


class RADAR_sub(Node):

    def __init__(self):
        super().__init__('POSE_Fixer')

        self.subscription = self.create_subscription(PoseArray,'/object/points',self.listener_callback,10)
        self.subscription  # prevent unused variable warning
        self.publisher = self.create_publisher(PoseArray, '/object/points_fixed', 10)

    def listener_callback(self, msg):
        out_msg = PoseArray()
        in_poses = msg.poses
        for i in in_poses:
            p = Pose()
            p.position.z = i.position.z - 0.8
            p.position.y = i.position.y
            p.position.x = i.position.x + 2.6
            out_msg.poses.append(p)
    
        out_msg.header.stamp = self.get_clock().now().to_msg()
        out_msg.header.frame_id = 'velodyne32'
        self.get_logger().info(f'Recieved msg')
        self.publisher.publish(out_msg)

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