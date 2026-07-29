---
name: github-actions-oidc
description: Authenticate to clouds via OIDC without static secrets.
---

# GitHub Actions OIDC

**Trigger**: Use when deploying to AWS, Azure, GCP, or Vault from Actions without storing long-lived cloud credentials.

## How OIDC Works

GitHub issues a short-lived JWT that cloud providers trust — no static secrets needed.

```yaml
permissions:
  id-token: write    # Required for OIDC
```

## AWS

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com

aws iam create-role --role-name github-actions-deploy \
  --assume-role-policy-document '{
    "Version":"2012-10-17",
    "Statement":[{
      "Effect":"Allow",
      "Principal":{"Federated":"arn:aws:iam::ACCOUNT:oidc-provider/token.actions.githubusercontent.com"},
      "Action":"sts:AssumeRoleWithWebIdentity",
      "Condition":{"StringEquals":{
        "token.actions.githubusercontent.com:aud":"sts.amazonaws.com",
        "token.actions.githubusercontent.com:sub":"repo:owner/repo:ref:refs/heads/main"
      }}
    }]
  }'
```

```yaml
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::ACCOUNT:role/github-actions-deploy
      aws-region: us-east-1
  - run: aws s3 sync ./dist s3://my-bucket
```

## Azure

```bash
az ad app create --display-name "github-actions-deploy"
az ad app federated-credential create --id <app-id> \
  --parameters '{"name":"github-actions","issuer":"https://token.actions.githubusercontent.com","subject":"repo:owner/repo:ref:refs/heads/main","audiences":["api://AzureADTokenExchange"]}'
```

```yaml
steps:
  - uses: azure/login@v2
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

## GCP

```bash
gcloud iam workload-identity-pools create "github-pool" --location="global"
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --location="global" --workload-identity-pool="github-pool" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub"
```

```yaml
steps:
  - uses: google-github-actions/auth@v2
    with:
      workload_identity_provider: "projects/PROJECT/locations/global/workloadIdentityPools/github-pool/providers/github-provider"
      service_account: "deploy-sa@project.iam.gserviceaccount.com"
```

## Subject Claims

| Scope | Subject |
|-------|---------|
| Main branch | `repo:owner/repo:ref:refs/heads/main` |
| Any branch | `repo:owner/repo:ref:refs/heads/*` |
| PR | `repo:owner/repo:pull_request` |
| Environment | `repo:owner/repo:environment:production` |

## Pitfalls
- **`id-token: write` required**: OIDC fails silently without this permission
- **Token lifetime**: 10 minutes — sufficient for deployments
- **Audience values**: AWS=`sts.amazonaws.com`, Azure=`api://AzureADTokenExchange`

## Verification
```bash
# Debug in workflow
- run: |
    curl -H "Authorization: bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" \
      "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=sts.amazonaws.com" | jq .value
```
