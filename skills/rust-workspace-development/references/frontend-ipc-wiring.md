# React/Tauri Frontend Wiring Pattern

## Rule

Frontend views must never call Tauri IPC directly. All IPC goes through a single typed API module.

## Files

- `src/cubeApi.ts` — imports `invoke` from `@tauri-apps/api/core` and exports typed async functions.
- `src/cw.d.ts` — TypeScript interfaces for requests/responses, kept in sync with Rust command signatures.
- `src/views/*.tsx` — import from `cubeApi.ts` only.

## Example `cubeApi.ts` shape

```ts
import { invoke } from '@tauri-apps/api/core';

export type CubeResponse = {
  id: string;
  genome_version: number;
  sex: string;
  fitness: number;
};

export type BreedRequest = {
  parent_a: string;
  parent_b: string;
  seed?: number[];
};

export async function createCube(req: { name: string; sex: string; seed?: number[] }): Promise<CubeResponse> {
  return invoke<CubeResponse>('create_cube', { req });
}

export async function breedCubes(req: BreedRequest): Promise<CubeResponse[]> {
  return invoke<CubeResponse[]>('breed_cubes', { req });
}

export async function getCube(id: string): Promise<CubeResponse> {
  return invoke<CubeResponse>('get_cube', { id });
}

export async function listCubes(): Promise<CubeResponse[]> {
  return invoke<CubeResponse[]>('list_cubes');
}
```

## Example `cw.d.ts` shape

```ts
export interface CubeResponse {
  id: string;
  genome_version: number;
  sex: string;
  fitness: number;
}

export interface BreedRequest {
  parent_a: string;
  parent_b: string;
  seed?: number[];
}
```

## Rule

Every Rust `#[tauri::command]` must have a matching typed export in `cubeApi.ts`. Every view must import from `cubeApi.ts`. Never call `invoke()` directly in a view.

## Verification

- `grep -r "invoke<" src/views` should return zero results.
- `grep -r "from '../cubeApi'" src/views` should show all views importing the wrapper.
- Rust `generate_handler![...]` list must match `cubeApi.ts` exports one-to-one.
