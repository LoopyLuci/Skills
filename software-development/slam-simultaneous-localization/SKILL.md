---
name: slam-simultaneous-localization
description: "Use when implementing SLAM for robotics."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [SLAM, localization, mapping, robotics, lidar, visual-SLAM, GMapping]
    related_skills: [ros-robot-operating-system, robot-control-systems, computer-vision-techniques, computer-vision]
---

# SLAM — Simultaneous Localization and Mapping

Implementing SLAM for robotics — from Lidar SLAM (GMapping, Cartographer) through Visual SLAM (ORB-SLAM), loop closure, and sensor fusion.

## When to Use

- Building robot that navigates unknown environments
- Generating maps from sensor data for autonomous navigation
- Localizing robot within existing map
- Visual-inertial odometry for AR/VR
- Autonomous vehicle localization

## SLAM Approaches

```python
SLAM_APPROACHES = {
    'lidar_slam': 'GMapping, Cartographer, Karto — 2D/3D lidar, grid maps, loop closure',
    'visual_slam': 'ORB-SLAM3, DSO, SVO — camera-only, feature-based or direct',
    'visual_inertial': 'VINS-Mono, OKVIS — camera + IMU fusion, robust to rapid motion',
    'multi_sensor': 'Lidar + camera + IMU + GPS — sensor fusion for robust SLAM',
}

class SLAMPipeline:
    """SLAM pipeline components."""
    
    STATE_ESTIMATION = ['Odometry', 'Scan matching (ICP)', 'Graph optimization', 'Loop closure detection']
    
    @staticmethod
    def evaluate_slam(estimated_path: np.array, ground_truth: np.array) -> Dict:
        from evo.core import metrics
        ape = metrics.APE(metrics.PosePath3D(estimated_path), metrics.PosePath3D(ground_truth))
        return {
            'rmse': round(ape.RMSE, 4),
            'mean': round(ape.mean, 4),
            'std': round(ape.std, 4),
        }
```

## Verification Checklist

- [ ] SLAM approach chosen (lidar, visual, visual-inertial)
- [ ] Sensor calibration performed (camera intrinsics, IMU biases, extrinsics)
- [ ] Loop closure detection working (recognizing revisited places)
- [ ] Map quality evaluated (consistency, drift over distance)
- [ ] Real-time performance (processing time < sensor frame rate)
- [ ] Localization accuracy measured (ATE, RPE metrics)
- [ ] Degenerate cases handled (featureless environments, rapid motion)
