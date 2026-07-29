---
name: ai-fairness-mitigation
description: "Use when detecting and mitigating bias in AI systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [fairness, bias, ethical-ai, auditing, responsible-ai]
    related_skills: [adversarial-ml-robustness, explainable-ai-xai-patterns, differential-privacy-training, agent-safety-alignment]
---

# AI Fairness and Bias Mitigation

Detecting, measuring, and mitigating bias in AI systems — from dataset auditing through model debiasing to post-deployment monitoring.

## When to Use

- Auditing ML models for fairness before deployment
- Building models for sensitive domains (hiring, lending, criminal justice)
- Regulatory compliance requiring fairness testing (EU AI Act, NYC Law 144)
- Debugging models that perform differently across demographic groups
- Implementing responsible AI practices in your ML pipeline

## Fairness Metrics

```python
import numpy as np
from sklearn.metrics import confusion_matrix

class FairnessMetrics:
    """Compute standard fairness metrics across demographic groups."""
    
    @staticmethod
    def demographic_parity(y_pred, sensitive_attr):
        """P(y_hat=1 | A=a) should be equal for all groups.
        Also called statistical parity."""
        groups = np.unique(sensitive_attr)
        rates = {}
        for group in groups:
            mask = sensitive_attr == group
            rates[group] = y_pred[mask].mean()
        return rates
    
    @staticmethod
    def equal_opportunity(y_true, y_pred, sensitive_attr):
        """TPR should be equal across groups.
        P(y_hat=1 | y=1, A=a) should be equal."""
        groups = np.unique(sensitive_attr)
        rates = {}
        for group in groups:
            mask = (sensitive_attr == group) & (y_true == 1)
            if mask.sum() > 0:
                rates[group] = y_pred[mask].mean()
            else:
                rates[group] = None
        return rates
    
    @staticmethod
    def equalized_odds(y_true, y_pred, sensitive_attr):
        """TPR and FPR should both be equal across groups."""
        groups = np.unique(sensitive_attr)
        result = {}
        for group in groups:
            cm = confusion_matrix(y_true[sensitive_attr == group], 
                                 y_pred[sensitive_attr == group])
            tn, fp, fn, tp = cm.ravel()
            result[group] = {
                'tpr': tp / (tp + fn) if (tp + fn) > 0 else None,
                'fpr': fp / (fp + tn) if (fp + tn) > 0 else None,
            }
        return result
    
    @staticmethod
    def disparate_impact(y_pred, sensitive_attr, privileged_group=1):
        """Ratio of positive prediction rates between unprivileged and privileged.
        0.8-1.25 is the 'four-fifths rule' threshold."""
        groups = np.unique(sensitive_attr)
        rates = {g: y_pred[sensitive_attr == g].mean() for g in groups}
        privileged_rate = rates.get(privileged_group, rates[max(rates)])
        return {
            g: rate / privileged_rate if privileged_rate > 0 else None
            for g, rate in rates.items()
        }
```

## Bias Detection Pipeline

```python
class BiasAuditor:
    """Full bias audit pipeline."""
    
    def audit_dataset(self, dataset, sensitive_attributes, target_column):
        """Audit training data for representation bias."""
        report = {}
        
        for attr in sensitive_attributes:
            # 1. Representation bias
            group_counts = dataset[attr].value_counts()
            report[f'{attr}_representation'] = group_counts.to_dict()
            
            # 2. Label bias
            for group in group_counts.index:
                group_data = dataset[dataset[attr] == group]
                pos_rate = group_data[target_column].mean()
                report[f'{attr}_label_rate_{group}'] = pos_rate
            
            # 3. Feature distribution similarity
            for col in dataset.select_dtypes(include=[np.number]).columns:
                if col not in sensitive_attributes + [target_column]:
                    ks_stat = self._ks_test(dataset, col, attr)
                    report[f'{col}_ks_by_{attr}'] = ks_stat
        
        return report
    
    def _ks_test(self, df, feature, sensitive_attr):
        """Kolmogorov-Smirnov test for distribution similarity."""
        from scipy.stats import ks_2samp
        groups = df[sensitive_attr].unique()
        if len(groups) == 2:
            g1 = df[df[sensitive_attr] == groups[0]][feature]
            g2 = df[df[sensitive_attr] == groups[1]][feature]
            return ks_2samp(g1, g2).statistic
        return None
    
    def audit_model(self, model, X_test, y_test, sensitive_attrs):
        """Audit model predictions for outcome bias."""
        y_pred = model.predict(X_test)
        
        report = {}
        for attr_name, attr_values in sensitive_attrs.items():
            report[attr_name] = {
                'demographic_parity': FairnessMetrics.demographic_parity(y_pred, attr_values),
                'equal_opportunity': FairnessMetrics.equal_opportunity(y_test, y_pred, attr_values),
                'equalized_odds': FairnessMetrics.equalized_odds(y_test, y_pred, attr_values),
                'disparate_impact': FairnessMetrics.disparate_impact(y_pred, attr_values),
            }
        
        return report
```

## Bias Mitigation Techniques

### Pre-processing: Dataset Re-weighting

```python
class Reweighting:
    """Re-weight training samples to ensure fairness."""
    
    def fit(self, X, y, sensitive_attr):
        """Compute sample weights for fairness."""
        groups = np.unique(sensitive_attr)
        weights = np.ones(len(X))
        
        for group in groups:
            group_mask = sensitive_attr == group
            pos_mask = group_mask & (y == 1)
            neg_mask = group_mask & (y == 0)
            
            # Weight so that each group's positive rate equals overall rate
            overall_pos_rate = y.mean()
            group_pos_rate = y[group_mask].mean()
            
            # Reweight
            weights[pos_mask] = overall_pos_rate / group_pos_rate if group_pos_rate > 0 else 0
            weights[neg_mask] = (1 - overall_pos_rate) / (1 - group_pos_rate) if group_pos_rate < 1 else 0
        
        return weights
```

### In-processing: Adversarial Debiasing

```python
import torch
import torch.nn as nn

class AdversarialDebiaser:
    """Adversarial debiasing: predictor tries to predict y while
    adversary tries to predict sensitive attribute from predictions."""
    
    def __init__(self, input_dim, hidden_dim=64, adv_weight=0.1):
        self.predictor = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
        self.adversary = nn.Sequential(
            nn.Linear(1, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)  # Binary sensitive attribute
        )
        self.adv_weight = adv_weight
    
    def train_step(self, X, y, sensitive, pred_opt, adv_opt):
        # Phase 1: Train predictor to minimize y loss AND fool adversary
        pred = self.predictor(X)
        pred_loss = F.binary_cross_entropy_with_logits(pred, y)
        
        adv_pred = self.adversary(pred.detach())
        adv_loss = F.binary_cross_entropy_with_logits(adv_pred, sensitive)
        
        # Predictor wants to maximize adversary loss (make it hard to predict S)
        total_loss = pred_loss - self.adv_weight * adv_loss
        
        pred_opt.zero_grad()
        total_loss.backward()
        pred_opt.step()
        
        # Phase 2: Train adversary to predict S from predictions
        pred = self.predictor(X).detach()
        adv_pred = self.adversary(pred)
        adv_loss = F.binary_cross_entropy_with_logits(adv_pred, sensitive)
        
        adv_opt.zero_grad()
        adv_loss.backward()
        adv_opt.step()
        
        return pred_loss.item(), adv_loss.item()
```

### Post-processing: Threshold Adjustment

```python
class ThresholdAdjuster:
    """Adjust decision thresholds per group to achieve fairness."""
    
    def find_equal_opportunity_thresholds(self, y_true, y_pred_proba, sensitive_attr):
        """Find per-group thresholds that equalize TPR."""
        groups = np.unique(sensitive_attr)
        thresholds = {}
        
        overall_tpr = None
        for group in groups:
            mask = sensitive_attr == group
            y_group = y_true[mask]
            scores = y_pred_proba[mask]
            
            if overall_tpr is None:
                # Use first group as reference
                best = self._find_threshold_for_tpr(scores, y_group)
                overall_tpr = best['tpr']
                thresholds[group] = best['threshold']
            else:
                # Match to reference TPR
                thresholds[group] = self._find_threshold_for_tpr(
                    scores, y_group, target_tpr=overall_tpr
                )
        
        return thresholds
```

## Monitoring

```python
class FairnessMonitor:
    """Post-deployment fairness monitoring."""
    
    def __init__(self, window_size=1000):
        self.window_size = window_size
        self.predictions = []
        self.outcomes = []
        self.sensitive_attrs = []
    
    def log_prediction(self, pred, actual_outcome, sensitive_attr):
        """Log a prediction for fairness monitoring."""
        self.predictions.append(pred)
        self.outcomes.append(actual_outcome)
        self.sensitive_attrs.append(sensitive_attr)
        
        # Keep sliding window
        if len(self.predictions) > self.window_size:
            self.predictions.pop(0)
            self.outcomes.pop(0)
            self.sensitive_attrs.pop(0)
    
    def check_drift(self):
        """Check if fairness metrics have drifted beyond threshold."""
        if len(self.predictions) < 100:
            return None
        
        metrics = FairnessMetrics()
        dp = metrics.demographic_parity(
            np.array(self.predictions),
            np.array(self.sensitive_attrs)
        )
        
        alerts = []
        for group, rate in dp.items():
            if abs(rate - 0.5) > 0.2:  # Threshold
                alerts.append(f"Demographic parity violation for {group}: {rate:.3f}")
        
        return alerts
```

## Common Pitfalls

1. **Fairness through blindness** — removing sensitive attributes doesn't remove bias (proxy features)
2. **Trade-off with accuracy** — fairness often reduces accuracy; document the trade-off
3. **Intersectionality** — bias at intersections (race × gender) is often worse than single-axis; test jointly
4. **Sampling bias in audit** — small sample sizes per group give unreliable metrics; require minimum counts
5. **Static fairness ≠ ongoing** — fairness degrades as data drifts; implement continuous monitoring
6. **Different fairness definitions conflict** — demographic parity and equal opportunity can't both be satisfied; choose based on context

## Verification Checklist

- [ ] Dataset audited for representation and label bias
- [ ] Model evaluated on at least 3 fairness metrics
- [ ] Disparate impact within 0.8-1.25 (four-fifths rule)
- [ ] Intersectional groups tested (race×gender, etc.)
- [ ] Mitigation technique applied if bias detected
- [ ] Post-deployment monitoring configured for fairness drift
- [ ] Fairness-accuracy trade-off documented

## See Also

- adversarial-ml-robustness — fairness as a robustness property
- explainable-ai-xai-patterns — understanding why bias occurs
- differential-privacy-training — privacy and fairness intersections
- agent-safety-alignment — ethical AI in agent systems
