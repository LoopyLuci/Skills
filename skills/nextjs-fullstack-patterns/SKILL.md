---
name: nextjs-fullstack-patterns
description: "Use when building fullstack apps with Next.js."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [nextjs, react, SSR, app-router, server-components, middleware]
    related_skills: [react-hooks-advanced, typescript-advanced-types, frontend-bootstrap]
---

# Next.js Fullstack Patterns

Building fullstack applications with Next.js — from App Router and Server Components through data fetching, middleware, and deployment.

## When to Use

- Building fullstack React applications with SSR/SSG
- Using Next.js App Router (13+)
- Server Components and Server Actions
- API routes and middleware

## Next.js Patterns

```typescript
// Server Component with data fetching
async function UserPage({ params }: { params: { id: string } }) {
  const user = await fetchUser(params.id); // Direct fetch, no useEffect
  return <div>{user.name}</div>;
}

// Server Action for form handling
'use server';
async function createUser(formData: FormData) {
  const name = formData.get('name');
  await db.user.create({ data: { name } });
  revalidatePath('/users');
}

// Route Handler (API route)
export async function GET(request: Request) {
  const users = await db.user.findMany();
  return Response.json(users);
}
```

## Verification Checklist

- [ ] Server Components default, Client Components opt-in
- [ ] Data fetching at component level (no waterfall)
- [ ] Server Actions for mutations
- [ ] ISR for static + dynamic hybrid
- [ ] Middleware for auth and redirects
- [ ] Route groups for layout organization
