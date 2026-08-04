---
name: cold-chain-logistics
description: "Use when managing cold chain logistics. Temperature control."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cold-chain, logistics, temperature-control, food-safety, pharma]
    related_skills: [supply-chain-optimization, food-tech-supply-chain]
---

# Cold Chain Logistics Management

## Overview
Design and operate temperature-controlled supply chains for perishable goods including food, pharmaceuticals, and biotech products. Covers cold storage facility design, refrigerated transport, temperature monitoring, HACCP compliance, traceability systems, and cold chain disruption mitigation.

## When to Use
- "Plan cold chain storage facilities"
- "Monitor temperature in transit"
- "Ensure HACCP compliance for cold storage"
- "Optimize refrigerated transport routes"
- "Trace perishable products through supply chain"

## Cold Storage Facility Design

### Temperature Zone Classification
| Zone | Temperature | Products | Insulation R-value |
|------|-------------|----------|-------------------|
| Frozen | -18°C to -25°C | Ice cream, frozen foods, vaccines | R-40+ |
| Fresh | -1°C to 4°C | Dairy, produce, fresh meat | R-30+ |
| Chilled Processing | 0°C to 10°C | Prep areas, packing zones | R-25+ |
| Ambient Controlled | 15°C to 25°C | Dry goods, packaging | R-15+ |

### Refrigeration System Selection
```python
def refrigeration_sizing(daily_cooling_load_kw, ambient_temp_c, desired_temp_c):
    """
    Size refrigeration system with safety factors
    
    Args:
        daily_cooling_load_kw: calculated cooling requirement (kW)
        ambient_temp_c: maximum ambient temperature (°C)
        desired_temp_c: target storage temperature (°C)
    
    Returns:
        Required refrigeration capacity with safety factors
    """
    # Add safety factor for defrost cycles, peak loads
    safety_factor = 1.3
    
    # Temperature lift factor
    temp_lift = ambient_temp_c - desired_temp_c
    lift_factor = 1 + (temp_lift / 50)  # Adjust for extreme conditions
    
    required_capacity = daily_cooling_load_kw * safety_factor * lift_factor
    
    return {
        "required_capacity_kw": round(required_capacity, 2),
        "compressor_selection": select_compressor(required_capacity),
        "energy_consumption_kwh_day": round(required_capacity * 24, 0),
        "backup_system_required": required_capacity > 10  # Redundancy for large systems
    }

def select_compressor(capacity_kw):
    """Select appropriate compressor based capacity"""
    if capacity_kw < 5:
        return "Hermetic reciprocating"
    elif capacity_kw < 50:
        return "Semi-hermetic scroll"
    elif capacity_kw < 200:
        return "Open screw"
    else:
        return "Centrifugal compressor"
```

## Temperature Monitoring & Control

### IoT Monitoring System
```python
class ColdChainMonitor:
    def __init__(self, sensors):
        self.sensors = sensors  # List of sensor objects
        self.alert_threshold_hot = 4.0  # °C above setpoint
        self.alert_threshold_cold = 5.0  # °C below setpoint
    
    def check_temperature_bounds(self):
        """
        Check all sensors for out-of-bounds temperatures
        """
        alerts = []
        for sensor in self.sensors:
            if sensor.is_out_of_bounds():
                alerts.append({
                    'sensor_id': sensor.id,
                    'location': sensor.location,
                    'current_temp': sensor.temperature,
                    'setpoint': sensor.setpoint,
                    'deviation': sensor.temperature - sensor.setpoint,
                    'severity': 'HIGH' if abs(sensor.temperature - sensor.setpoint) > 5 
                               else 'MEDIUM' if abs(sensor.temperature - sensor.setpoint) > 2 
                               else 'LOW'
                })
        return alerts
    
    def compliance_report(self, date_range):
        """
        Generate temperature compliance report for cold chain audit
        """
        data = self.get_historical_data(date_range)
        
        compliance = {
            'temperature_deviation_events': 0,
            'total_hours_monitored': len(data) * 24,
            'compliance_percentage': 0.0,
            'max_temp_recorded': 0.0,
            'min_temp_recorded': 0.0,
            'avg_temp': 0.0
        }
        
        # Calculate compliance (±0.5°C tolerance for frozen, ±1°C for chilled)
        out_of_bounds = [
            d for d in data 
            if abs(d['temperature'] - d['zone_setpoint']) > d['tolerance']
        ]
        
        compliance['temperature_deviation_events'] = len(out_of_bounds)
        compliance['compliance_percentage'] = round(
            (1 - len(out_of_bounds) / len(data)) * 100, 2
        )
        
        return compliance

# Example sensor monitoring class
class TemperatureSensor:
    def __init__(self, sensor_id, location, setpoint, tolerance=0.5):
        self.id = sensor_id
        self.location = location
        self.setpoint = setpoint
        self.tolerance = tolerance
        self.temperature = None
        self.timestamp = None
    
    def is_out_of_bounds(self):
        return (abs(self.temperature - self.setpoint) > self.tolerance 
                if self.temperature else False)
```

## Refrigerated Transport Optimization

### Route Planning for Cold Chain
```python
def cold_chain_route_planning(delivery_points, depot_temp, vehicle_specs):
    """
    Optimize delivery routes for temperature-sensitive goods
    """
    # Factors affecting cold chain integrity during transport
    transport_factors = {
        'distance_factor': 0.1,  # Temp rise per 100km
        'door_open_time_factor': 0.5,  # Temp rise per minute door open
        'ambient_temp_factor': 0.05,  # Temp influence of ambient temperature
        'engine_idle_factor': 0.02   # Cooling efficiency when engine running
    }
    
    # Route optimization with temperature constraints
    def temp_preservation_objective(route):
        """
        Minimize temperature excursions during transport
        """
        total_temp_rise = 0
        cumulative_distance = 0
        
        for i, point in enumerate(route[:-1]):
            distance = calculate_distance(point, route[i+1])
            cumulative_distance += distance
            
            # Temperature rise calculation
            ambient_effect = max(0, (point['ambient_temp'] - 25) * transport_factors['ambient_temp_factor'])
            distance_effect = distance * transport_factors['distance_factor'] / 100
            
            total_temp_rise += ambient_effect + distance_effect
        
        # Ensure max temp rise stays within tolerance
        return {
            "total_temp_rise_celsius": total_temp_rise,
            "within_tolerance": total_temp_rise <= 3.0,  # Max 3°C rise
            "estimated_deliveries": len(route) - 1,
            "total_distance_km": cumulative_distance
        }
    
    return temp_preservation_objective
```

## HACCP Compliance for Cold Chains

### Critical Control Points
| CCP | Monitoring | Critical Limit | Corrective Action |
|-----|------------|----------------|-------------------|
| Receiving | Temperature check | ≤4°C for chilled | Reject if >8°C |
| Storage | Continuous monitoring | -18°C ±2°C (frozen) | Adjust refrigeration |
| Transport | Pre-cooling time | ≤2 hours pre-cool | Delay shipment |
| Delivery | Delivery time | ≤2 hours from truck to customer | Expedite unloading |
| Transfer | Temperature during transfer | ±2°C tolerance | Immediate reefer restart |

## Traceability & Recall Management

### Blockchain-Based Traceability
```python
def traceability_record(product_id, batch_number, temperature_data):
    """
    Create immutable record for product traceability
    """
    from hashlib import sha256
    import json
    
    record = {
        'product_id': product_id,
        'batch_number': batch_number,
        'timestamp': datetime.utcnow().isoformat(),
        'temperature_readings': temperature_data,
        'location_history': get_location_history(product_id),
        'handling_events': get_handling_events(product_id),
        'hash': ''  # Placeholder for blockchain hash
    }
    
    # Generate hash for blockchain storage
    record['hash'] = sha256(
        json.dumps({k: v for k, v in record.items() if k != 'hash'}, sort_keys=True).encode()
    ).hexdigest()
    
    return record

def recall_traceability(batch_number):
    """
    Trace product backward/forward for recall execution
    """
    # Backward trace (find all ingredients/components)
    backward = find_upstream_components(batch_number)
    
    # Forward trace (find all customers who received this batch)
    forward = find_downstream_customers(batch_number)
    
    return {
        'batch': batch_number,
        'manufacturing_date': get_batch_info(batch_number)['manufactured_date'],
        'upstream_suppliers': backward,
        'downstream_customers': forward,
        'recall_priority': 'HIGH' if forward else 'NONE',
        'affected_locations': len(forward)
    }
```

## Common Pitfalls
1. **Insufficient temperature monitoring** — spot checks instead of continuous logging
2. **Not validating backup systems** — backup refrigeration fails during power outage
3. **Poor insulation or door design** — energy waste, temperature fluctuations
4. **Ignoring door-open frequency** — each opening = significant temperature rise
5. **Not training drivers** — improper loading, extended door open times
6. **No emergency procedures** — cold chain breaks without protocols
7. **Wrong packaging materials** — inadequate insulation for product type
8. **Not monitoring in-transit duration** — delays cause product spoilage
9. **Missing traceability** — cannot execute recalls efficiently
10. **No temperature mapping studies** — hot spots in warehouse undetected

## Verification Checklist
- [✓] Continuous temperature monitoring with datalogger alarms
- [✓] Backup refrigeration system tested monthly
- [✓] HACCP plan with all 4 critical control points identified
- [✓] Temperature mapping completed for all storage zones
- [✓] Refrigerated transport equipment pre-cooled before loading
- [✓] Delivery time ≤2 hours from warehouse to customer
- [✓] Temperature monitoring during transport (IoT sensors)
- [✓] Emergency procedures for cold chain breaks documented
- [✓] Full product traceability from farm to fork
- [✓] Recall simulation exercise completed successfully