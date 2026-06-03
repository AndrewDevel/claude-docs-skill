---
id: intro
title: Inicio / Home
slug: /
sidebar_position: 1
---

# {{PROJECT_NAME}}

<p>
  <span class="badge badge--post">{{STACK}}</span>&nbsp;
  <span class="badge badge--auth">v{{VERSION}}</span>
</p>

> 📅 Última actualización / Last updated: **{{DATE}}**

:::tip Documentación bilingüe / Bilingual docs
Cada página está en **español e inglés**. Usa el selector de idioma (arriba a la derecha) o las
pestañas dentro de cada sección. / Every page is in **Spanish and English**.
:::

## ¿Qué encontrarás aquí? / What you'll find here

<div class="card-grid">
  <a class="doc-card" href="tecnica/">
    <h3>🏗️ Técnica / Technical</h3>
    <p>Arquitectura, decisiones, setup, estructura y modelos de datos.</p>
  </a>
  <a class="doc-card" href="plataforma/">
    <h3>🧭 Plataforma / Platform</h3>
    <p>Onboarding y flujos paso a paso para el cliente final.</p>
  </a>
  <a class="doc-card" href="api/">
    <h3>🔌 API</h3>
    <p>Endpoints, autenticación y contratos con playground interactivo.</p>
  </a>
  <a class="doc-card" href="tecnica/pruebas">
    <h3>✅ Pruebas / Testing</h3>
    <p>Cómo correr tests, cobertura y estrategia de calidad.</p>
  </a>
</div>

<!-- Elimina las tarjetas que no apliquen al repo. / Remove cards that don't apply. -->

## Mapa rápido / Quick map

```mermaid
mindmap
  root(({{PROJECT_NAME}}))
    Técnica
      Arquitectura
      Setup
      Modelos de datos
    Plataforma
      Onboarding
      Flujos
    API
      Endpoints
      Auth
    Pruebas
      Unitarias
      E2E
```
