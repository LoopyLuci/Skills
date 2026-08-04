---
name: drone-crop-monitoring
description: "Use when monitoring crops with drones. Multispectral, NDVI."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [drones, agriculture, multispectral, ndvi, crop-monitoring]
    related_skills: [precision-agriculture, crop-yield-modeling]
---

# Drone-Based Crop Monitoring & Analysis

## Overview
Plan and execute drone-based crop monitoring programs using multispectral, RGB, and thermal sensors. Covers flight planning, image capture protocols, data processing pipelines, vegetation index calculation (NDVI, GNDVI), anomaly detection, and prescription map generation for precision agriculture.

## When to Use
- "Plan drone flights for crop monitoring"
- "Process multispectral imagery for NDVI analysis"
- "Detect crop stress with aerial data"
- "Generate prescription maps from drone data"
- "Set up automated crop scouting workflows"

## Flight Mission Planning

### Sensor Selection Matrix
| Sensor Type | Wavelength | Use Cases | Resolution |
|-------------|------------|-----------|------------|
| RGB | Visible (450-680nm) | Scouting, stand establishment | 12-20 MP |
| Multispectral | Multiple bands | NDVI, vegetation indices | 1.2-5 MP |
| Thermal | LWIR (8-14μm) | Water stress, disease detection | 640×512 |
| Hyperspectral | 100+ narrow bands | Species ID, nutrient status | 30+ bands |
| LiDAR | 905/1550nm | Topography, canopy height | <5cm |

### Flight Parameters Optimization
```python
def optimize_flight_parameters(field_size_ha, crop_type, growth_stage):
    """
    Determine optimal flight parameters for crop monitoring
    """
    # Altitude based on required resolution
    altitude_m = {
        'scouting': 30,      # High-res RGB for pest/disease
        'ndvi_mapping': 80,   # Standard multispectral
        'prescription': 120,  # Broad coverage mapping
        'height_modeling': 50  # Canopy height with LiDAR
    }
    
    # Overlap requirements
    overlap_pct = 80  # Front overlap
    sidelap_pct = 70  # Side overlap
    
    # Flight speed (m/s)
    flight_speed = 5  # Slower for multispectral quality
    
    # Time of day constraints
    sun_angle_min = 30  # Minimum sun elevation for quality illumination
    capture_window = "9:00-14:00"  # Best lighting window
    
    # Calculate flight plan
    coverage_width = calculate_coverage_width(altitude_m['ndvi_mapping'])
    flight_lines = calculate_flight_lines(field_size_ha, coverage_width, sidelap_pct)
    
    return {
        "altitude_m": altitude_m['ndvi_mapping'],
        "overlap_pct": overlap_pct,
        "sidelap_pct": sidelap_pct,
        "flight_speed_ms": flight_speed,
        "capture_window": capture_window,
        "estimated_flights": len(flight_lines),
        "estimated_time_minutes": len(flight_lines) * field_size_ha / 10
    }

def calculate_coverage_width(altitude_m):
    """
    Calculate ground coverage width based altitude and sensor FOV
    """
    # Example for MicaSense RedEdge sensor (FOV ~23°)
    coverage_width = 2 * altitude_m * math.tan(math.radians(23/2))
    return round(coverage_width, 1)  # meters
```

## Image Processing Pipeline

### Vegetation Indices Calculation
```python
import numpy as np
import rasterio

class VegetationIndexCalculator:
    def __init__(self, multispectral_data):
        self.blue = multispectral_data['blue']
        self.green = multispectral_data['green']
        self.red = multispectral_data['red']
        self.red_edge = multispectral_data['red_edge']
        self.nir = multispectral_data['nir']
    
    def calculate_ndvi(self):
        """
        NDVI = (NIR - Red) / (NIR + Red)
        Range: -1 to 1 (healthy vegetation ~0.3-0.8)
        """
        ndvi = (self.nir.astype(float) - self.red.astype(float)) / \
               (self.nir.astype(float) + self.red.astype(float))
        return np.clip(ndvi, -1, 1)
    
    def calculate_gndvi(self):
        """
        GNDVI = (NIR - Green) / (NIR + Green)
        Better for chlorophyll content
        """
        gndvi = (self.nir.astype(float) - self.green.astype(float)) / \
               (self.nir.astype(float) + self.green.astype(float))
        return np.clip(gndvi, -1, 1)
    
    def calculate_ndre(self):
        """
        NDRE = (NIR - RedEdge) / (NIR + RedEdge)
        Sensitive to nitrogen content
        """
        ndre = (self.nir.astype(float) - self.red_edge.astype(float)) / \
               (self.nir.astype(float) + self.red_edge.astype(float))
        return np.clip(ndre, -1, 1)
    
    def detect_stress_areas(self, ndvi_threshold=0.4):
        """
        Identify areas with low vegetation health
        """
        ndvi = self.calculate_ndvi()
        
        # Classify vegetation health
        health_classes = {
            'optimal': (0.6, 1.0),      # Dark green, healthy
            'good': (0.4, 0.6),          # Green, good health
            'stressed': (0.2, 0.4),      # Yellow, stressed
            'severe_stress': (-1.0, 0.2) # Bare soil/dead vegetation
        }
        
        anomaly_mask = ndvi < ndvi_threshold
        anomaly_areas = np.where(anomaly_mask, 255, 0).astype(np.uint8)
        
        return {
            'ndvi_map': ndvi,
            'health_classification': classify_by_ranges(ndvi, health_classes),
            'stress_areas_mask': anomaly_areas,
            'stress_area_count': np.sum(anomaly_mask),
            'stress_percentage': round(np.mean(anomaly_mask) * 100, 1)
        }
```

## Anomaly Detection & Prescription Maps

### Machine Learning for Anomaly Detection
```python
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans

def generate_prescription_map(ndvi_data, soil_data, historical_data):
    """
    Generate variable rate prescription maps
    """
    # Combine all data sources
    features = np.column_stack([
        ndvi_data.flatten(),
        soil_data['organic_matter'].flatten(),
        soil_data['ph'].flatten(),
        soil_data['phosphorus'].flatten(),
        historical_data['yield'].flatten()
    ])
    
    # Anomaly detection for stress areas
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    anomalies = iso_forest.fit_predict(features)
    
    # Cluster-based zone management
    kmeans = KMeans(n_clusters=4, random_state=42)
    zones = kmeans.fit_predict(features)
    
    # Generate prescriptions per zone
    prescriptions = {}
    for zone_id in range(4):
        zone_mask = (zones == zone_id).reshape(ndvi_data.shape)
        zone_ndvi = ndvi_data[zone_mask].mean()
        zone_yield = historical_data['yield'][zone_mask].mean()
        
        # Nitrogen prescription based on NDVI deviation from field avg
        avg_ndvi = ndvi_data.mean()
        ndvi_deficit = avg_ndvi - zone_ndvi
        
        if ndvi_deficit > 0.1:  # Significant deficit
            n_prescription = 150  # lbs N/acre supplemental
        elif ndvi_deficit > 0.05:
            n_prescription = 100
        else:
            n_prescription = 50  # Maintenance level
        
        prescriptions[f'Zone_{zone_id}'] = {
            'avg_ndvi': round(float(zone_ndvi), 3),
            'avg_yield': round(float(zone_yield), 1),
            'nitrogen_prescription_lbs': n_prescription,
            'zone_area_ha': round(float(np.sum(zone_mask) * pixel_area_ha), 2)
        }
    
    return prescriptions
```

## Flight Safety & Compliance

### Pre-Flight Checklist
```python
def pre_flight_checklist(drone_config, mission_plan, weather_data):
    """
    Comprehensive pre-flight safety checklist
    """
    checks = {
        'drone_status': {
            'battery_level': drone_config['battery_percent'] >= 95,
            'gps_signal': drone_config['gps_satellites'] >= 8,
            'imu_calibration': drone_config['imu_calibrated'],
            'compass_calibration': drone_config['compass_calibrated'],
            'propeller_check': drone_config['props_ok'],
            'camera_gimbal': drone_config['gimbal_ok']
        },
        'mission_plan': {
            'boundary_valid': validate_mission_boundary(mission_plan['boundary']),
            'waypoint_altitude_safe': all(wp['altitude'] > 10 and wp['altitude'] < 120 
                                         for wp in mission_plan['waypoints']),
            'no_fly_zone_check': check_nofly_zones(mission_plan['center'])
        },
        'weather': {
            'wind_speed': weather_data['wind_speed'] <= 14,  # mph
            'visibility': weather_data['visibility'] >= 5,   # km
            'cloud_cover': weather_data['cloud_cover'] <= 30, # %
            'precipitation': weather_data['precip_prob'] <= 10
        }
    }
    
    all_pass = all(all(v.values()) for v in checks.values())
    
    return {
        'all_checks_passed': all_pass,
        'failed_checks': [item for section in checks.values()
                         for item in section if not section[item]],
        'recommendation': 'LAUNCH' if all_pass else 'ABORT_MISSION'
    }
```

## Data Integration Framework

### Connecting to Farm Management Software
```python
def sync_drone_data_to_fms(fms_api_url, drone_data_batch):
    """
    Push processed drone analytics to farm management system
    """
    # Transform drone data to FMS format
    transformed_data = {
        'timestamp': drone_data_batch['flight_timestamp'],
        'field_id': drone_data_batch['field_id'],
        'analytics': {
            'ndvi_mean': drone_data_batch['ndvi_mean'],
            'ndvi_std': drone_data_batch['ndvi_std'],
            'stress_areas': drone_data_batch['stress_area_pct'],
            'prescription_map_url': drone_data_batch['prescription_url']
        },
        'sensor_metadata': {
            'flight_id': drone_data_batch['flight_id'],
            'sensor_model': drone_data_batch['sensor_model'],
            'capture_time': drone_data_batch['end_time']
        }
    }
    
    # API call to farm management system
    response = requests.post(
        f"{fms_api_url}/api/v1/field_analytics",
        json=transformed_data,
        headers={'Authorization': f'Bearer {os.environ["FMS_API_KEY"]}'},
        timeout=30
    )
    
    if response.status_code == 200:
        return {'status': 'success', 'record_id': response.json()['record_id']}
    else:
        return {'status': 'error', 'message': response.text}
```

## Common Pitfalls
1. **Flying at wrong altitude** — too high loses resolution, too low wastes time
2. **Poor lighting conditions** — flying at wrong time reduces imagery quality
3. **Inadequate ground control points** — poor geolocation accuracy
4. **Not calibrating sensors** — incorrect reflectance values in multispectral data
5. **Ignoring flight regulations** — FAA Part 107, local drone laws
6. **Cloud shadows skewing NDVI** — need to filter cloud-contaminated images
7. **Over-processing imagery** — losing detail in aggressive resampling
8. **Wrong interpretation of indices** — NDVI doesn't mean what you think in all crops
9. **No ground truth data** — NDVI maps need validation with actual field data
10. **Data overload** — collecting too much imagery without actionable outcomes

## Verification Checklist
- [✓] Flight altitude optimized for required resolution
- [✓] Weather conditions checked (wind <14 mph, visibility >5km)
- [✓] Sensors calibrated before each flight
- [✓] Flight plan validated with no-fly zone check
- [✓] Ground control points established for accuracy
- [✓] NDVI calculations validated against ground sampling
- [✓] Prescription maps generated with actionable rates
- [✓] Data uploaded to FMS with proper metadata
- [✓] Flight logs reviewed for compliance/regulatory audit
- [✓] Anomalies ground-truthed before treatment recommendation