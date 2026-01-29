# Improved_Fast-lio2_ROS2_with--hybrid-icp

1.

run Fast-lio and play ros2 bag (.mcap)

Terminal 1 (Fast-LIO)

    source /opt/ros/jazzy/setup.bash
    source ~/ros2_ws/install/setup.bash
    ros2 launch fast_lio mapping.launch.py config_file:=mid360.yaml


Terminal 2 (bag)

    source /opt/ros/jazzy/setup.bash
    source ~/ros2_ws/install/setup.bash
    ros2 bag play ~/ws_livox/bags/3_Senario-2/d/combined.mcap/combined.mcap_0.mcap --clock


if you rebuild 

    cd ~/ros2_ws
    source /opt/ros/jazzy/setup.bash
    rm -rf build install log
    colcon build --symlink-install 
    
or 

    colcon build --packages-select FAST_LIO_ROS2
    source install/setup.bash

 
 Terminal 3 — Paste the Python exporter (THIS ONE)

 ----------------------------------------------------------------------------------------------

    source /opt/ros/jazzy/setup.bash
    source ~/ros2_ws/install/setup.bash

    mkdir -p ~/fastlio_output
    cd ~/fastlio2_output

    
    cd ~/fastlio2_output
    
    python3 - <<'PY'
    import os
    import rclpy
    from rclpy.node import Node
    from nav_msgs.msg import Odometry

    OUT_PATH = os.path.abspath("trajectory.tum")

    class OdomToTUM(Node):
        def __init__(self):
            super().__init__('odom_to_tum')
            self.count = 0
            self.out = open(OUT_PATH, 'w', buffering=1)
            self.sub = self.create_subscription(Odometry, '/Odometry', self.cb, 50)
            self.get_logger().info(f"Subscribing to /Odometry and writing TUM to: {OUT_PATH}")

        def cb(self, msg: Odometry):
            t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
            p = msg.pose.pose.position
            q = msg.pose.pose.orientation
            self.out.write(
                f"{t:.9f} {p.x:.6f} {p.y:.6f} {p.z:.6f} "
                f"{q.x:.6f} {q.y:.6f} {q.z:.6f} {q.w:.6f}\n"
            )
            self.count += 1
            if self.count % 200 == 0:
                self.get_logger().info(f"Wrote {self.count} poses...")

    def main():
        rclpy.init()
        node = OdomToTUM()
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass
        node.get_logger().info(f"Stopping. Total poses written: {node.count}")
       node.out.close()
        node.destroy_node()
        rclpy.shutdown()

    if __name__ == "__main__":
        main()
    PY
