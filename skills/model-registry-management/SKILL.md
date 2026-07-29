---
name: model-registry-management
description: "Use when managing ML model versions and registries."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [model-registry, model-versioning, deployment, governance, staging, production]
    related_skills: [ml-experiment-tracking, ml-deployment-serving, ml-pipeline-design, model-evaluation-metrics]
---

# Model Registry Management

Managing ML model versions, staging, approval workflows, and deployment through a model registry — from tracking model artifacts through governance and production monitoring.

## When to Use

- Tracking multiple model versions across environments
- Managing model promotion (staging → production)
- Implementing model governance and audit trails
- Automating model deployment pipelines
- Monitoring model performance in production

## Registry Architecture

```python
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json
import os

class ModelStage(str, Enum):
    NONE = 'none'
    STAGING = 'staging'
    PRODUCTION = 'production'
    ARCHIVED = 'archived'

class ModelStatus(str, Enum):
    PENDING = 'pending_review'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    ROLLED_BACK = 'rolled_back'

class ModelRegistry:
    """Track and manage ML model versions."""
    
    def __init__(self, registry_path: str = './model_registry'):
        self.path = registry_path
        os.makedirs(registry_path, exist_ok=True)
    
    def register_model(self, name: str, version: str, 
                       model_path: str, metrics: Dict,
                       params: Dict = None, framework: str = 'pytorch',
                       description: str = '') -> Dict:
        """Register a new model version."""
        metadata = {
            'name': name, 'version': version,
            'model_path': model_path, 'framework': framework,
            'metrics': metrics, 'params': params or {},
            'description': description,
            'stage': ModelStage.NONE.value,
            'status': ModelStatus.PENDING.value,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'registered_by': None,
            'approvals': [],
            'lineage': {'source_run': None, 'dataset_version': None},
        }
        
        # Save to registry
        reg_path = f"{self.path}/{name}/{version}"
        os.makedirs(reg_path, exist_ok=True)
        with open(f"{reg_path}/metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return metadata
    
    def promote_to_staging(self, name: str, version: str, 
                           approved_by: str = None) -> bool:
        """Promote model to staging."""
        meta = self._load_metadata(name, version)
        if not meta: return False
        
        meta['stage'] = ModelStage.STAGING.value
        meta['updated_at'] = datetime.now().isoformat()
        meta['approvals'].append({
            'action': 'promote_staging', 'by': approved_by,
            'time': datetime.now().isoformat(),
        })
        self._save_metadata(name, version, meta)
        return True
    
    def promote_to_production(self, name: str, version: str,
                               approved_by: str = None) -> bool:
        """Promote model to production. Demotes current production."""
        meta = self._load_metadata(name, version)
        if not meta: return False
        
        # Archive current production model
        current_prod = self.get_production_model(name)
        if current_prod:
            self._load_metadata(name, current_prod['version'])['stage'] = ModelStage.ARCHIVED.value
        
        meta['stage'] = ModelStage.PRODUCTION.value
        meta['status'] = ModelStatus.APPROVED.value
        meta['updated_at'] = datetime.now().isoformat()
        meta['approvals'].append({
            'action': 'promote_production', 'by': approved_by,
            'time': datetime.now().isoformat(),
        })
        self._save_metadata(name, version, meta)
        return True
    
    def get_production_model(self, name: str) -> Optional[Dict]:
        """Get the current production model for a name."""
        versions = self.list_versions(name)
        for v in reversed(versions):
            meta = self._load_metadata(name, v)
            if meta and meta['stage'] == ModelStage.PRODUCTION.value:
                return meta
        return None
    
    def list_versions(self, name: str) -> List[str]:
        model_dir = f"{self.path}/{name}"
        if not os.path.exists(model_dir): return []
        return sorted(os.listdir(model_dir))
    
    def compare_versions(self, name: str, versions: List[str]) -> str:
        report = f"📊 Model: {name} — Version Comparison\n" + "=" * 50 + "\n"
        for v in versions:
            meta = self._load_metadata(name, v)
            if meta:
                report += f"\nv{v}: {meta['stage']}"
                for metric, value in meta.get('metrics', {}).items():
                    report += f"\n  {metric}: {value}"
                report += f"\n  Params: {meta.get('params', {})}"
        return report
```

## Governance and Approvals

```python
class ModelGovernance:
    """Model governance and approval workflows."""
    
    def __init__(self, required_approvals: int = 2):
        self.required = required_approvals
    
    def approve(self, registry: ModelRegistry, name: str, 
                version: str, reviewer: str, notes: str = '') -> Dict:
        meta = registry._load_metadata(name, version)
        if not meta: return {'error': 'Model not found'}
        
        meta['approvals'].append({
            'action': 'approve', 'by': reviewer, 'notes': notes,
            'time': datetime.now().isoformat(),
        })
        
        # Check if enough approvals
        approvals = [a for a in meta['approvals'] if a['action'] == 'approve']
        if len(approvals) >= self.required:
            meta['status'] = ModelStatus.APPROVED.value
        
        registry._save_metadata(name, version, meta)
        return meta
    
    def audit_trail(self, registry: ModelRegistry, name: str, 
                    version: str) -> str:
        meta = registry._load_metadata(name, version)
        if not meta: return "Model not found"
        
        trail = f"📋 Audit Trail: {name} v{version}\n" + "=" * 50 + "\n"
        trail += f"Created: {meta['created_at']}\n"
        trail += f"Metrics: {meta['metrics']}\n"
        trail += f"Stage: {meta['stage']}\n"
        trail += "\nApprovals:\n"
        for a in meta.get('approvals', []):
            trail += f"  {a['time']} — {a['action']} by {a.get('by', 'system')}\n"
        return trail
```

## Common Pitfalls

1. **No versioning** — overwriting model files loses history; always version
2. **Manual promotion** — human error in moving models to production; automate the pipeline
3. **No staging validation** — promoting to production without staging validation causes incidents
4. **Missing lineage** — can't trace which training run or data produced a model
5. **No rollback plan** — if production model fails, need to quickly revert

## Verification Checklist

- [ ] Model registry tracks all model versions
- [ ] Staging → production promotion workflow defined
- [ ] Approval gates for production deployment
- [ ] Rollback procedure documented and tested
- [ ] Model lineage tracked (training run, dataset version)
- [ ] Model performance monitored in production
- [ ] Audit trail available for compliance

## See Also

- ml-experiment-tracking — experiment tracking feeding into registry
- ml-deployment-serving — deploying registered models
- ml-pipeline-design — CI/CD for model registry
- model-evaluation-metrics — evaluating models before registration
