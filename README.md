# DigiNexSynapse 🧠⚡

> **Autonomous Multi-Agent Orchestration Platform**  
> *Developed for the Kiroween 2026 Hackathon — "Skeleton Crew" Track*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Kiro Protocol](https://img.shields.io/badge/Kiro-MCP%202026-blue.svg)](https://github.com/topics/mcp)
[![Skeleton Crew](https://img.shields.io/badge/Track-Skeleton%20Crew-orange.svg)]()

---

## 📖 Overview

**DigiNexSynapse** is an autonomous multi-agent orchestration architecture designed to decouple telemetry routing and incident remediation into coordinated, specialized micro-agents. Built on top of a unified "Skeleton Crew" core, the platform enforces rigid, anti-hallucination agent steering via Model Context Protocol (MCP) standards while demonstrating dual-stack operational execution:

1. **App1 (`App1-Dynamic-API-Router`)**: A reactive Node.js routing gateway that ingests external API events, validates payload schemas, and autonomously dispatches tasks to registered Kiro MCP agents.
2. **App2 (`App2-Incident-Resolver`)**: An intelligent Python agent that continuously monitors incident error logs, extracts semantic features, and performs vector cosine similarity search against historical postmortems to trigger deterministic remediation.

Both applications share the foundational steering policies established in `/.kiro/steering.md` to prevent non-deterministic agent hallucinations.

---

## 🏗️ Repository Architecture ("Skeleton Crew")

```text
DigiNexSynapse/
├── App1-Dynamic-API-Router/         # Application 1: Node.js MCP Gateway
│   ├── package.json                 # Node.js project manifest & scripts
│   ├── index.js                     # Kiro MCP routing engine & HTTP interface
│   └── .env.example                 # Environment variable template
├── App2-Incident-Resolver/          # Application 2: Python Vector Remediation
│   ├── requirements.txt             # ML/AI dependencies (NumPy, Scikit-Learn)
│   ├── main.py                      # Cosine similarity log analyzer & resolver
│   └── .env.example                 # Environment variable template
├── .kiro/                           # Shared Kiro Protocol Configuration
│   └── steering.md                  # Strict anti-hallucination system prompt
├── .gitignore                       # Node & Python ignore rules (preserves .kiro)
├── LICENSE                          # Permissive MIT Open Source License
└── README.md                        # Master project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- **Node.js**: v18.0.0 or higher
- **Python**: v3.9 or higher
- **Git**

---

### Running App 1: Dynamic API Router (Node.js)

The API router operates an HTTP server that dispatches payloads through the mock Kiro MCP registry.

1. **Navigate to App1 directory**:
   ```bash
   cd App1-Dynamic-API-Router
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   ```

3. **Install dependencies (Optional)**:
   ```bash
   npm install
   ```

4. **Launch the router**:
   ```bash
   node index.js
   # or with npm:
   npm start
   ```

5. **Test the Kiro MCP routing endpoint**:
   ```bash
   curl -X POST http://localhost:3000/api/route \
     -H "Content-Type: application/json" \
     -d '{"eventType": "incident.resolve", "severity": "CRITICAL", "source": "prod-cluster-east-node4", "message": "Connection pool exhausted"}'
   ```

---

### Running App 2: Incident Resolver (Python)

The Incident Resolver computes vector cosine similarity between incoming runtime error logs and historical outage playbooks.

1. **Navigate to App2 directory**:
   ```bash
   cd App2-Incident-Resolver
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute incident analysis**:
   ```bash
   python main.py
   ```

---

## 🎯 Kiro Steering Protocols (`/.kiro/steering.md`)

All autonomous agents operating within DigiNexSynapse are constrained by the master steering directive located at `/.kiro/steering.md`. Key guardrails include:

- **Strict Schema Adherence**: Actions must be bounded by validated tool definitions.
- **Zero Extrapolation**: Agents are forbidden from hypothesizing unverified system topologies.
- **Graceful Escalation**: Automated actions degrade gracefully to human engineers when similarity scores fall below threshold.
- **Typed JSON Dispatch**: All inter-agent communications comply with the 2026 Model Context Protocol (MCP) format.

---

## 📄 License

This project is licensed under the open-source **MIT License** — see the [LICENSE](LICENSE) file for details.
