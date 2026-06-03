---
title: Documentación técnica / Technical documentation
sidebar_position: 1
---

# Documentación técnica / Technical documentation

> Última actualización / Last updated: {{DATE}} · Versión / Version: {{VERSION}}
> Stack: {{STACK}}

## Español

### 1. Visión general

{{OVERVIEW_ES}}

### 2. Arquitectura

{{ARCHITECTURE_ES}}

<!-- Si es útil, incluir un diagrama Mermaid: -->
```mermaid
flowchart LR
  A[Cliente] --> B[{{LAYER_1}}]
  B --> C[{{LAYER_2}}]
```

### 3. Estructura del repositorio

```
{{REPO_TREE}}
```

### 4. Decisiones de diseño

{{DESIGN_DECISIONS_ES}}

### 5. Modelos de datos

{{DATA_MODELS_ES}}

### 6. Setup del entorno

```bash
{{SETUP_COMMANDS}}
```

Variables de entorno:

| Variable | Descripción | Requerida |
| -------- | ----------- | --------- |
{{ENV_VARS_TABLE}}

---

## English

### 1. Overview

{{OVERVIEW_EN}}

### 2. Architecture

{{ARCHITECTURE_EN}}

### 3. Repository structure

See the tree above.

### 4. Design decisions

{{DESIGN_DECISIONS_EN}}

### 5. Data models

{{DATA_MODELS_EN}}

### 6. Environment setup

Same commands as above. Environment variables are listed in the Spanish section.
