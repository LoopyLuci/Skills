---
name: serverless-computing-patterns
description: "Use when building serverless applications and functions."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [serverless, lambda, functions, FaaS, AWS, cold-start, event-driven]
    related_skills: [event-driven-architecture, microservices-decomposition, ci-cd-pipeline-setup, terraform-module-patterns]
---

# Serverless Computing Patterns

Building serverless applications — from function design and event sources through cold-start optimization, observability, and cost management.

## When to Use

- Event-driven data processing pipelines
- APIs with variable traffic patterns
- Scheduled batch jobs and cron replacements
- Webhook handlers and integrations
- Prototyping and rapid iteration

## Function Design

```python
# Handler pattern (AWS Lambda + API Gateway)
def handler(event, context):
    """
    Standard Lambda handler for API Gateway HTTP API.
    """
    try:
        # Parse request
        path = event.get('rawPath', '/')
        method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        
        # Business logic
        result = process_request(method, path, body)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result)
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
```

## Common Pitfalls

1. **Cold starts** — functions spin up from zero on infrequent invocations; use provisioned concurrency
2. **Timeout limits** — Lambda max 15 min; design for the limit or use Step Functions
3. **Stateless assumption** — no local filesystem state between invocations; use S3/EFS
4. **Over-fragmentation** — one function per endpoint = management nightmare; group related logic
5. **Cost surprises** — high invocation rates cost more than fixed servers; estimate first

## Verification Checklist

- [ ] Cold start time < 500ms (or acceptable for use case)
- [ ] Function timeout matches expected execution time
- [ ] Error handling with DLQ for async invocations
- [ ] Tracing/monitoring configured (X-Ray, CloudWatch)
- [ ] Least-privilege IAM roles per function
- [ ] Environment variables for configuration (not code)
- [ ] Versioning and aliases for safe deployments
