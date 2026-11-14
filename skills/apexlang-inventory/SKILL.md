---
name: apexlang-inventory
description: Use when working with provides an overview of APEX application components, APEXlang syntax, and application file layout, with links to detailed component properties and examples.
version: 2.0.0
author: LoopyLuci Community
license: UPL-1.0
platforms: [any]
metadata:
  hermes:
    tags: [oracle, apex, apexlang]
    source: oracle/skills
    adapted: true
---

# APEXLang Component Catalog

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Provides an overview of APEX application components, APEXlang syntax, and application file layout, with links to detailed component properties and examples. Use this catalog to select, compose, generate, and edit APEX applications with APEXlang

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Routing index for APEXlang application components (APEX 26.2.0). Use the hierarchy to locate the detailed references under `assets/`, then read the matching component document before authoring. A referenced document with a `filePath` bullet represents a component declared in its own APEX application file; the full catalog lives in `assets/` — read only the documents needed for the current `.apx` file.

## Authoring sequence

1. Start from the application layout and create `application.apx` with an `app` component.
2. Select a component from the catalog and open its linked document under `assets/`.
3. Use the document's `componentType` and `identifierRequired` bullets to write the declaration; use its `filePath` only when the component is the root of its own `.apx` file.
4. Add the documented properties by group name: a `(direct group)` is flattened into the component, other groups use `{ ... }`; complex properties use `property: { ... }`, arrays use `property: [ ... ]`, and nested components use `componentType identifier ( ... )`.
5. Follow the catalog hierarchy for containment. Choose `plugin-variants/<plugin-name>` or `template-component/<name>` only after checking the parent or ancestor selector and its applicability condition.
6. Validate the completed application before deploying it.

Every property, array value, group member, and nested component member goes on its own physical line, using APEXlang-visible enum values and component references rather than internal metadata or display labels.

## Reading a component document

- `componentType` is the APEXlang declaration keyword; the directory name, link text, and node path are routing labels and may differ from it.
- `identifierRequired` decides whether the declaration needs an identifier.
- Each property bullet is one property line, using the documented property name and the APEXlang enum value rather than its descriptive label.
- `filePath` is the component's location in the application, not a property to emit inside it.
- `appliesWhen` is a selection condition based on required parent or ancestor values, not an APEXlang property.
- In an `appliesWhen` condition, `component[group.property]` identifies a property on another component: `menu[identification.type]` and `menu[behavior.type]` are different properties despite sharing the name `type`. Conditions joined by `and` must all hold; alternatives joined by `or` are separate valid choices.

For a plugin-specific component, inspect the relevant parent or ancestor component's type property and applicability conditions, then follow the matching `plugin-variants/<plugin-name>` node. For a template component, inspect the parent or ancestor and the current-theme applicability, then follow `template-component/<name>`; its APEXlang plugin value is `themeTemplateComponent/<name>`. The `componentType` bullet in the referenced Markdown file is authoritative.

## Minimal application layout

- `application.apx` — top-level manifest with app-level settings such as navigation (home link, login link, navigation menu); declares the `app` component and is the entry point of the hierarchy.
- `.apex/apexlang.json` — APEXLang metadata for the export.
- `deployments/default.json` — deployment metadata, including app id and debug flag.
- `pages/*.apx` — one page per file, named `p<zero-padded-5-digit-page-number>-<normalized-page-name>.apx` unless the component's `filePath` constrains it. No subdirectories; each file declares a page component.
- `shared-components/` — components usable on any page: lists, LOVs, breadcrumbs, app items, computations, authentications, authorizations, automations, task definitions, plugins, theme files, static assets.
  - `authentications.apx` — how users authenticate.
  - `lists.apx` — reusable data sources for regions.
  - `static-files/icons/` — application icons.
  - `themes/<theme-name>/theme.apx` — theme settings; at least one theme is required.

## Rules

When using `supportingObject`, make sure its scripts run automatically during deployment: `advanced.includeInAppExport = autoInstall`.

## Syntax mapping

- A property bullet becomes one line, `name: value`.
- A group marked `(direct group)` is not emitted as a block — emit its properties directly, e.g. `name: Orders`.
- Any other group is a property group: its name has no colon, e.g. `layout {`, followed by its properties.
- A property documented as `<COMPLEX>` is object-valued: `target: {`, followed by its properties.
- An array-valued property also has a colon: `templateOptions: [`, one value per line.
- A nested component is another declaration, e.g. `region CONTENT (` — not a group and not an object.
- Opening braces and brackets may share a line with their name, but their contents start on the next line.
- Every property, array value, and nested member is on its own physical line; closing braces, brackets, and component parentheses are on their own line.
- A scalar property holds exactly one scalar value on one line.

## Invalid forms

Inline property group — invalid:

```apexlang
layout { sequence: 10 slot: body }
```

Valid:

```apexlang
layout {
    sequence: 10
    slot: body
}
```

Property group written as an object — invalid (`layout: {`), valid (`layout {`).

Complex property written as a group — invalid (`target {`), valid (`target: {`).

Inline complex object — invalid (`target: { page: 15 action: resetPagination }`), valid (properties on separate lines).

Inline array — invalid (`templateOptions: [#DEFAULT# t-Button--hot]`), valid (one value per line).

Nested component mistaken for a group — invalid (`region { name: Orders }`), valid (`region ORDERS ( name: Orders )`).

## Component catalog

The complete catalog is under `assets/`; each entry links to `assets/<slug>/<slug>.md`. `plugin-variants/` and `template-component/` are routing categories, not component types. Main groupings:

- **Application services** — webCredential, restEnabledSqlDatabase, authenticationServer, printServer, restDataSourceServer, fileServer, file, appGroup, genAIService, vectorProvider.
- **App-level** — the `app` root with aiAgent (and tool/parameter), appComputation, appItem, appProcess (and executeCode), appSetting, authentication (and its scheme variants), authorization (and its variants), automation (and action/parameter), theme (styles, templates, slots, options), breadcrumb (and entry), buildOption, classicNavigationBarEntry, componentGroup (and component), componentSetting, concatenatedFile, dataLoadDefinition (and dataProfileColumn), developerComment, dynamicTranslation, emailTemplate, jsonDualityView, jsonSource, pageGroup, plugin (attributes, slots, events, files), pwaScreenshot, pwaShortcut, reportLayout, reportQuery (and sourceQuery), restDataSource (operations, variants, synchronization), role, searchConfig, shortcut, substitution, supportingObject (install/upgrade scripts, validation, buildOption), taskDefinition, textMessage, workflow (versions, activities, participants, variables).
- **Page-level** — page with page items, regions (and their many plugin variants), validations, buttons, dynamic actions.
- **Theme** — page, region, list, button, classic-report, field, breadcrumb, and popup-LOV templates, template options and option groups, theme styles and files.

## Further instructions

- Read the matching reference under `assets/` before authoring; follow nested paths to preserve APEXlang containment.
- Only a component type that defines its own `filePath` is a root component for that application file. Nested components, plugin variants, and template components do not display an inherited ancestor path; ancestor paths are used internally only when resolving a descendant with its own file boundary.
- `assets/` is relative to this `SKILL.md`. Its directories represent node-path segments, usually slugified, and a directory name is not necessarily the compiler `componentType`.
- Property bullets use: `name` — `type`; `description`; `Yes|No` (required or optional); `default`; `enum:[option:"Description", ...]`; `constraints`; `nestedCondition`. An em dash means the field does not apply or is omitted; only applicable fields are included. Enum entries are APEXlang values.
- Before selecting a plugin variant, inspect the relevant parent or ancestor type property and the variant's `appliesWhen`. For template components, `app[userInterface.currentTheme]` must satisfy the condition.
- Load lazily: read only the component references required for the current file, and use only the properties defined on the list.

## Verification

- [ ] `application.apx` declares the `app` root; pages follow the `p<page>-<name>.apx` convention.
- [ ] Each component's `componentType` and `identifierRequired` taken from its `assets/` document.
- [ ] One property, array value, group member, and nested member per physical line; closers on their own line.
- [ ] Only documented properties used, with APEXlang enum values rather than labels.
- [ ] Plugin and template variants selected via parent type and `appliesWhen`.
- [ ] Application validated before deployment.

## Related Skills in This Repo

- [oke-troubleshooter](../oke-troubleshooter/SKILL.md) — Use when the user wants to diagnose or root-cause issues with an OCI Kubernetes Engine clu...
- [oke-gva-deployer](../oke-gva-deployer/SKILL.md) — Use when the user asks to enable, deploy, or configure Generic VNIC Attachment (GVA) for O...
- [oci-functions-deploy](../oci-functions-deploy/SKILL.md) — Use when asked to validate/install Fn, OCI CLI, and Docker, configure or create Fn context...
- [oke-cluster-generator](../oke-cluster-generator/SKILL.md) — Use when the user asks to build, generate, create, design, or scaffold an OKE (OCI Kuberne...

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [oracle/skills](https://github.com/oracle/skills)
- Path: `_sources/oracle_skills/apex/apexlang/26.2/apexlang-inventory/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
