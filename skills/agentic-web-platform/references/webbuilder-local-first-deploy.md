# Local-First Deployment Pattern

This reference covers the local-first deployment architecture used by WebBuilder, where projects can run on bare metal, containers, or cloud.

## Deployment Targets

| Environment | Technology | Use Case |
|-------------|------------|----------|
| **Local** | `npm run dev` | Development |
| **Bare Metal** | systemd service | Self-hosted production |
| **Docker** | Multi-stage Dockerfile | Container deployment |
| **Docker Compose** | docker-compose.yml | Multi-container apps |
| **Kubernetes** | Deployment + Service +Ingress | Orchestration |
| **Vercel** | API adapter | Serverless |
| **Netlify** | API adapter | Static/JAMstack |
| **Cloudflare** | Pages API | Edge deployment |

## Bare Metal Deployment

```ini
# /etc/systemd/system/webbuilder.service
[Unit]
Description=WebBuilder Server
After=network.target

[Service]
Type=simple
User=webbuilder
WorkingDirectory=/opt/webbuilder
ExecStart=/usr/bin/node dist/cli.js --host 0.0.0.0 --port 3000 --mode production
Restart=on-failure
RestartSec=5
Environment=NODE_ENV=production

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/opt/webbuilder/data

# Resource limits
MemoryMax=512M
CPUQuota=50%

[Install]
WantedBy=multi-user.target
```

## Docker Multi-Stage Build

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS base
WORKDIR /app
RUN corepack enable pnpm

FROM base AS deps
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY packages/*/package.json ./packages/*/
RUN pnpm install --frozen-lockfile

FROM base AS build
COPY --from=deps /app/node_modules ./node_modules
COPY packages ./packages
RUN pnpm -r build

FROM base AS production
ENV NODE_ENV=production
COPY --from=build /app/packages/server/dist ./dist
COPY --from=build /app/packages/server/package.json ./package.json
RUN pnpm install --prod --frozen-lockfile

EXPOSE 3000
CMD ["node", "dist/cli.js", "--host", "0.0.0.0", "--port", "3000"]
```

## Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webbuilder
spec:
  replicas: 1
  selector:
    matchLabels:
      app: webbuilder
  template:
    metadata:
      labels:
        app: webbuilder
    spec:
      containers:
        - name: webbuilder
          image: webbuilder/server:latest
          ports:
            - containerPort: 3000
          env:
            - name: NODE_ENV
              value: "production"
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /api/health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: webbuilder
spec:
  selector:
    app: webbuilder
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: ClusterIP
```

## Export Module

```typescript
// packages/server/src/export.ts
export interface ExportOptions {
  projectDir: string;
  projectName: string;
  environments: ('local' | 'docker' | 'kubernetes' | 'vercel' | 'netlify' | 'cloudflare')[];
}

export async function exportProject(options: ExportOptions): Promise<ExportResult> {
  const files: string[] = [];
  const instructions: string[] = [];

  for (const env of options.environments) {
    switch (env) {
      case 'local':
        files.push(...exportLocal(options.projectDir, options.projectName));
        instructions.push('Run: npm install && npm run dev');
        break;
      case 'docker':
        files.push(...exportDocker(options.projectDir, options.projectName));
        instructions.push('Run: docker-compose up -d');
        break;
      case 'kubernetes':
        files.push(...exportKubernetes(options.projectDir, options.projectName));
        instructions.push('Run: kubectl apply -f deploy/kubernetes/');
        break;
    }
  }

  return { success: true, files, instructions };
}
```

## Pitfall: Port Conflicts

When starting multiple Next.js dev servers (web app + test projects), port 3000 conflicts are common. Always check for existing processes:

```bash
# Check what's on port 3000
netstat -ano | findstr :3000

# Or kill all node processes (careful!)
tasklist | grep node | awk '{print $2}' | xargs -r taskkill //PID
```

## Pitfall: MCP Server Discovery in Hermes

When adding MCP servers to Hermes, the `setup_mcp` tool requires the server to be in the Hermes catalog. For custom/local servers, use `hermes config` commands instead:

```bash
hermes config set mcp_servers.webbuilder.command node
hermes config set mcp_servers.webbuilder.args '["C:/Projects/WebBuilder/packages/mcp-server/dist/cli.js"]'
hermes config set mcp_servers.webbuilder.timeout 120
hermes config set mcp_servers.webbuilder.connect_timeout 60
```

After config changes, **restart Hermes** for MCP servers to load.
