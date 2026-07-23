# RulesApp — Maritime Regulatory Knowledge Base & Engineering Repository

**Version**: 1.0.0-alpha.1  
**Publisher**: Marine Intelligence Weekly (MIW)  
**Target Platform**: Offline Web Application & Native Windows Desktop Application (`.NET 7.0-windows` / WebView2)  
**Architecture Status**: **FROZEN (Version 1.x)**  

---

## 1. Project Purpose

**RulesApp** is a document-centric, offline-first maritime regulatory knowledge repository and engineering evaluation engine designed specifically for Marine Engineers, Chief Engineers, and MEO Class 1 examination candidates.

Rather than providing a flat list of regulations or un-indexed PDF documents, RulesApp:
* Decomposes IMO conventions, codes, resolutions, IRS classification rules, and DG Shipping circulars down to paragraph-level statutory provisions.
* Establishes typed, bidirectional cross-references (`depends_on`, `amends`, `supersedes`, `complements`).
* Connects real-world vessel machinery (Boilers, Steering Gear, Emergency Generators, OWS, Fixed CO2, EGCS) to every provision that governs it via **Engineering Objects**.
* Exposes **Official Context Views** (`Official Regulation`, `Official Chapter`, `Document Info`) for continuous, un-altered statutory reading alongside engineering interpretations.

---

## 2. Architecture Overview

RulesApp follows a strict decoupled, 3-tier architecture:

```text
┌─────────────────────────────────────────────────────────────────┐
│                      Client Layer (app/)                        │
│  - Vanilla HTML5 / CSS3 / JavaScript (No heavy frameworks)      │
│  - Zero network runtime dependencies; 100% offline              │
│  - 4-Tab Detail Panel (Engineering, Regulation, Chapter, Info)  │
└───────────────────────────────┬─────────────────────────────────┘
                                │ Synchronous Fetch API
┌───────────────────────────────▼─────────────────────────────────┐
│               Generated Index Layer (repository/index/)        │
│  - repo-data.json, search-index.json, crossref-graph.json        │
│  - Compiled deterministically by Node.js build pipeline         │
└───────────────────────────────▲─────────────────────────────────┘
                                │ Build Pipeline (repository/build/)
┌───────────────────────────────┴─────────────────────────────────┐
│            Authoritative Source Store (repository/)             │
│  - standards/, definitions/, engineering-objects/, schema/      │
│  - Human-editable JSON files enforcing Version 1.0 JSON Schema  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Repository Overview

```text
F:\RulesApp\
├── app/                        <-- Offline Client Web UI (HTML/CSS/JS)
│   ├── css/style.css           <-- Design system & visual tokens
│   ├── js/                     <-- Core database (db.js), search (search.js), render (render.js), nav (nav.js)
│   └── js/views/               <-- Specialized workflow views (advanced search, crossref, study)
├── desktop/                    <-- Native Windows Desktop Application
│   └── RulesAppDesktop/        <-- WPF C# project (.NET 7.0-windows / WebView2)
├── repository/                 <-- Authoritative Source Data Store (Source of Truth)
│   ├── build/                  <-- Node.js build pipeline & quality gates
│   ├── definitions/            <-- Cross-cutting defined terms (29 definitions)
│   ├── engineering-objects/    <-- Equipment hubs (26 engineering objects)
│   ├── governance/             <-- Architectural Decision Records (ADRs 1–8)
│   ├── index/                  <-- Client search & relationship index artifacts
│   ├── media/                  <-- Technical diagrams & media assets
│   ├── organizations/          <-- Regulatory bodies (IMO, IRS, DGMA)
│   ├── schema/                 <-- JSON Schemas enforcing node structure
│   └── standards/              <-- 78 Decomposed Standards & 788 Node provisions
├── index.html                  <-- Root Launch Portal landing page
├── CHANGELOG.md                <-- Documented version history
└── .gitignore                  <-- Production git ignore rules
```

---

## 4. Build Instructions & Pipeline

### **Prerequisites**:
* **Node.js**: v18.0 or higher
* **.NET SDK**: v7.0 or higher (for building the native Windows desktop application)

### **A. Node.js Repository Build Pipeline**:
Run the following build pipeline commands from the root directory:

```bash
# 1. Validate JSON schemas, references, and relationships
node repository/build/validate.js

# 2. Execute health check audit
node repository/build/health-check.js

# 3. Compile client search and relationship indexes (builds repository/index/*.json)
node repository/build/build-index.js

# 4. Run performance latency and memory review
node repository/build/performance-review.js
```

### **B. Native Windows Desktop Application Build**:
To publish the native Windows C# WPF / WebView2 application:

```bash
# Framework-Dependent Build (Requires .NET 7.0 Desktop Runtime on target PC):
dotnet publish desktop/RulesAppDesktop/RulesAppDesktop.csproj -c Release -o desktop/publish

# Self-Contained Standalone Build (RECOMMENDED: Includes embedded runtime, zero setup):
dotnet publish desktop/RulesAppDesktop/RulesAppDesktop.csproj -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -o desktop/publish-standalone
```

---

## 5. Workflows

### **Developer Workflow**:
1. Edit or add decomposed standards in `repository/standards/`.
2. Edit or add cross-cutting defined terms in `repository/definitions/`.
3. Edit or add equipment links in `repository/engineering-objects/`.
4. Run `node repository/build/validate.js` and `node repository/build/build-index.js`.
5. Open `app/index.html` in browser or run `desktop/publish/RulesAppDesktop.exe` to verify.

### **Founder Workflow (Acceptance & Audit)**:
1. Launch `desktop/publish-standalone/RulesAppDesktop.exe`.
2. Execute natural Chief Engineer searches (`II-1/29`, `aux steering`, `CO₂`, `OWS 15 ppm`, `SOx`, `NOx Tier III`).
3. Toggle between `🛠 Engineering View`, `📖 Official Regulation`, `📚 Official Chapter`, and `ℹ️ Document Info`.
4. Verify breadcrumb navigation links (`IMO › SOLAS 1974 › Chapter II-1 › Regulation 29 › Paragraph 29.3`).

---

## 6. Repository Philosophy & Offline-First Principles

* **Offline-First**: RulesApp operates 100% locally from compiled JSON indexes. No cloud APIs, no external databases, no telemetry tracking.
* **Statutory Integrity**: Official statutory wording is preserved verbatim without paraphrasing. Engineering commentary is strictly isolated in dedicated views.
* **Deterministic Build**: Every client index file in `repository/index/` is compiled deterministically from human-readable source JSON files.

---

## 7. Future Roadmap & Architectural Decision Records (ADRs)

* **Architectural Governance**: All design decisions are documented in Architectural Decision Records under `repository/governance/adrs/`:
  - `adr_0001`: Offline JSON Repository Architecture
  - `adr_0002`: Node Decomposition & Unique ID Schema
  - `adr_0003`: Engineering Object Mapping Architecture
  - `adr_0008`: Search Normalization & Alias Expansion
* **Version 2.0 Roadmap**: Future expansion will introduce the **Statutory Applicability Engine** (evaluating vessel keel-laying date, gross tonnage, and ship type parameters dynamically).

---

*RulesApp Version 1.0 Alpha — Built by Marine Intelligence Weekly.*
