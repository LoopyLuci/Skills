---
name: ros-robot-operating-system
description: "Use when building robotics applications with ROS."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ROS, robotics, robot-operating-system, navigation, perception, control]
    related_skills: [robot-control-systems, slam-simultaneous-localization, computer-vision-techniques, agent-environment-interaction]
---

# Robot Operating System (ROS)

Building robotics applications with ROS — from nodes and topics through navigation stacks, sensor integration, and robot control.

## When to Use

- Developing robot control and perception systems
- Implementing sensor integration (lidar, cameras, IMU)
- Building robot navigation and path planning
- Multi-robot coordination and communication

## ROS Fundamentals

```python
ROS_CONCEPTS = {
    'nodes': 'Individual processes that perform computation',
    'topics': 'Pub-sub bus for data streams (sensor data, commands)',
    'services': 'Request-reply for one-shot interactions',
    'actions': 'Long-running tasks with feedback (navigation, arm control)',
    'tf': 'Coordinate transforms between frames (map, odom, base_link)',
}

# ROS 2 Python node pattern
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class PatrolRobot(Node):
    def __init__(self):
        super().__init__('patrol_robot')
        self.sub = self.create_subscription(LaserScan, 'scan', self.scan_callback, 10)
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
    
    def scan_callback(self, msg):
        cmd = Twist()
        if min(msg.ranges) < 0.5:
            cmd.angular.z = 0.5  # Turn away from obstacle
        else:
            cmd.linear.x = 0.2  # Move forward
        self.pub.publish(cmd)
"""
```

## Verification Checklist

- [ ] ROS distribution chosen (ROS 2 Humble/Iron recommended)
- [ ] Node architecture designed with clear topic/service boundaries
- [ ] TF tree defined for coordinate transforms
- [ ] Navigation stack (Nav2) configured for robot
- [ ] Sensor drivers integrated (lidar, camera, IMU, odometry)
- [ ] Simulation in Gazebo or Ignition for testing
- [ ] Real-time constraints considered (if applicable)
