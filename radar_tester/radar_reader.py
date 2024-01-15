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
        self.cars_publisher = self.create_publisher(PoseArray, '/object/cars', 10)
        self.pedestrians_publisher = self.create_publisher(PoseArray, '/object/pedestrians', 10)

    def listener_callback(self, msg):
        poses_msg = PoseArray()
        cars = PoseArray()
        pedestrians = PoseArray()
        objs = msg.tracks
        for i in objs:
            p = Pose()
            p.position.z = i.position.z - 0.8
            p.position.y = i.position.y
            p.position.x = i.position.x + 2.2
            poses_msg.poses.append(p)

            if i.classification == 32001:
                cars.poses.append(p)
                self.get_logger().info(f'Found a car!!!!')
            elif i.classification == 32007:
                pedestrians.poses.append(p)
                self.get_logger().info(f'Found a pedestrian!!!!')
        
            self.get_logger().info(f'{i.classification}, {i.NO_CLASSIFICATION}, {i.STATIC}, {i.DYNAMIC}')
    
        poses_msg.header.stamp = self.get_clock().now().to_msg()
        poses_msg.header.frame_id = 'velodyne32'
        self.publisher.publish(poses_msg)

        cars.header.stamp = self.get_clock().now().to_msg()
        cars.header.frame_id = 'velodyne32'
        self.cars_publisher.publish(cars)

        pedestrians.header.stamp = self.get_clock().now().to_msg()
        pedestrians.header.frame_id = 'velodyne32'
        self.pedestrians_publisher.publish(pedestrians)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = RADAR_sub()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()