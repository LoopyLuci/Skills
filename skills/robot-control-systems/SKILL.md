---
name: robot-control-systems
description: "Use when implementing robot control systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [robot-control, PID, LQR, MPC, kinematics, dynamics, trajectory]
    related_skills: [ros-robot-operating-system, slam-simultaneous-localization, agent-environment-interaction, deep-reinforcement-learning]
---

# Robot Control Systems

Implementing robot control systems — from PID and LQR through Model Predictive Control (MPC), kinematics, dynamics, and trajectory optimization.

## When to Use

- Building control systems for robotic arms or mobile robots
- Implementing PID or state-space control
- Trajectory planning and tracking
- Balancing, walking, or flying robot control

## Control Methods

```python
import numpy as np

class PIDController:
    """PID controller for robot joint/velocity control."""
    def __init__(self, kp: float, ki: float, kd: float, dt: float = 0.01):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.dt = dt
        self.integral = 0
        self.prev_error = 0
    
    def compute(self, setpoint: float, measurement: float) -> float:
        error = setpoint - measurement
        self.integral += error * self.dt
        derivative = (error - self.prev_error) / self.dt
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative

class DifferentialDrive:
    """Differential drive robot kinematics."""
    def __init__(self, wheel_radius: float, track_width: float):
        self.r = wheel_radius
        self.L = track_width
    
    def forward_kinematics(self, left_w: float, right_w: float) -> Dict:
        """Wheel velocities → robot velocities."""
        v = self.r * (left_w + right_w) / 2
        omega = self.r * (right_w - left_w) / self.L
        return {'linear_x': v, 'angular_z': omega}
    
    def inverse_kinematics(self, v: float, omega: float) -> Dict:
        """Robot velocities → wheel velocities."""
        left = (v - omega * self.L / 2) / self.r
        right = (v + omega * self.L / 2) / self.r
        return {'left_wheel': left, 'right_wheel': right}
```

## Verification Checklist

- [ ] Control method chosen (PID, LQR, MPC) based on system dynamics
- [ ] Kinematic model validated (forward and inverse)
- [ ] PID gains tuned (Ziegler-Nichols or auto-tuning)
- [ ] State estimation integrated (sensor feedback, Kalman filter)
- [ ] Trajectory tracking accuracy measured (RMS error)
- [ ] Safety limits (velocity, acceleration, torque limits)
- [ ] Real-time control loop verified (cycle time < 10ms)
- [ ] Fault detection (encoder errors, motor stalls)
