# 🛰️ AstraGuard — AI Space Debris Collision Avoidance Co-Pilot

> **"Physics calculates. AI decides. Operators approve."**

AstraGuard is an AI-powered space traffic management system that tracks orbital objects in real-time, detects dangerous conjunction events (close approaches between satellites and space debris), and leverages **IBM Granite AI** to recommend optimal collision-avoidance maneuvers with explainable reasoning.

![AstraGuard Demo](docs/demo-screenshot.png)

---

## 🚨 Problem Statement

Low Earth Orbit (LEO) is dangerously congested with over **35,000 tracked pieces of space debris** traveling at velocities up to 28,000 km/h. Satellite operators receive thousands of Conjunction Data Messages (CDMs) weekly, but:

- **Manual analysis is slow** — engineers must evaluate collision probability, mission constraints, and fuel budgets under extreme time pressure
- **Decision fatigue is real** — most alerts are false alarms, but missing a real threat can destroy a multi-billion-dollar asset
- **No unified decision support** — operators juggle spreadsheets, orbital mechanics software, and experience-based intuition

A single collision can generate thousands of new debris fragments, triggering a **Kessler Syndrome** cascade that threatens the entire orbital infrastructure humanity depends on for GPS, communications, weather monitoring, and national security.

---

## 💡 Solution Description

AstraGuard acts as an **intelligent air-traffic control co-pilot for Earth orbit**. It provides:

1. **Automated Orbital Tracking** — Ingests live Two-Line Element (TLE) data from CelesTrak to track satellites and debris in real-time
2. **Conjunction Detection** — Uses SGP4 orbital propagation to predict close approaches within a 72-hour window
3. **Multi-Factor Risk Scoring** — Evaluates each conjunction on miss distance, relative velocity, object type, and orbital uncertainty
4. **Maneuver Option Generation** — Calculates three avoidance strategies (Conservative, Balanced, Minimal) with delta-V, fuel cost, and safety margin trade-offs
5. **AI-Powered Decision Support** — IBM Granite analyzes all factors and recommends the optimal maneuver with detailed, explainable reasoning
6. **Human-in-the-Loop Approval** — Operators review the AI recommendation, examine the evidence, and approve with a single click

### Key Differentiator
> **Physics calculates. AI decides. Operators approve.**
>
> AstraGuard never asks the AI to compute orbital mechanics — that's done by validated SGP4 algorithms. Instead, IBM Granite reasons over the computed physics results alongside mission constraints, fuel budgets, and risk tolerance to provide intelligent, explainable decision support.

---

## 🧠 AI Approach & Architecture

### Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                     ASTRAGUARD SYSTEM                         │
│                                                              │
│  ┌─────────────┐    ┌────────────────────┐    ┌───────────┐ │
│  │  CelesTrak   │───▶│   PYTHON BACKEND   │◀──▶│  NEXT.JS  │ │
│  │  TLE Feed    │    │    (FastAPI)        │    │ FRONTEND  │ │
│  └─────────────┘    │                    │    │           │ │
│                      │  ┌──────────────┐  │    │ 🌍 Globe   │ │
│                      │  │ SGP4 Orbital  │  │    │ 📊 Dash    │ │
│                      │  │ Propagator   │  │    │ 🚨 Alerts  │ │
│                      │  └──────────────┘  │    │ 🤖 AI      │ │
│                      │         │          │    │           │ │
│                      │         ▼          │    └───────────┘ │
│                      │  ┌──────────────┐  │                  │
│                      │  │ Conjunction   │  │                  │
│                      │  │ Detector     │  │                  │
│                      │  └──────────────┘  │                  │
│                      │         │          │                  │
│                      │         ▼          │                  │
│                      │  ┌──────────────┐  │                  │
│                      │  │ Risk Scorer  │  │                  │
│                      │  └──────────────┘  │                  │
│                      │         │          │                  │
│                      │         ▼          │                  │
│                      │  ┌──────────────┐  │                  │
│                      │  │ Maneuver Gen │  │                  │
│                      │  └──────────────┘  │                  │
│                      │         │          │                  │
│                      │         ▼          │                  │
│                      │  ┌──────────────┐  │                  │
│                      │  │ IBM GRANITE  │  │                  │
│                      │  │ AI ADVISOR   │  │                  │
│                      │  └──────────────┘  │                  │
│                      └────────────────────┘                  │
└──────────────────────────────────────────────────────────────┘
```

### AI Components

| Component | Technology | Role |
|---|---|---|
| **Orbital Propagation** | SGP4 (Python `sgp4` library) | Calculates satellite positions and trajectories using validated orbital mechanics |
| **Conjunction Detection** | Custom algorithm + NumPy | Identifies close approaches by propagating all objects forward and computing pairwise distances |
| **Risk Assessment** | Multi-factor scoring model | Evaluates conjunction severity using distance, velocity, object size, and uncertainty |
| **Decision Intelligence** | **IBM Granite via watsonx** | Analyzes computed physics results + mission constraints to recommend optimal avoidance maneuver |
| **Explainability** | **IBM Granite via watsonx** | Generates human-readable operator briefings explaining WHY the recommendation is safe |

### Why IBM Granite?

AstraGuard uses IBM Granite not as a simple chatbot, but as a **mission-critical decision reasoning engine**:

1. **Multi-constraint reasoning** — Granite weighs fuel budget, mission priority, orbital lifetime impact, and collision probability simultaneously
2. **Trade-off analysis** — Explains why one maneuver option is better than alternatives in the operator's specific context
3. **Secondary risk assessment** — Evaluates whether the proposed maneuver creates NEW conjunction risks with other objects
4. **Operator briefing generation** — Produces clear, evidence-based briefings that operators can trust and verify

---

## 🏷️ Challenge Theme

**Space Exploration** — AstraGuard directly addresses the challenge of making space operations safer, smarter, and more accessible through AI-powered decision support for satellite collision avoidance.

---

## 🔧 How IBM Bob Was Used

AstraGuard was developed entirely using **IBM Bob** as the primary development environment:

- **Architecture Design** — Used Bob to plan the system architecture and component interactions
- **Code Generation** — Bob generated the FastAPI backend, React frontend, and API integration code
- **Debugging & Testing** — Bob assisted with identifying and fixing orbital mechanics edge cases
- **Documentation** — Bob helped write this README and code documentation

---

## 🛠️ Tech Stack

### Backend
- **Python 3.11+** — Core language
- **FastAPI** — High-performance REST API framework
- **sgp4** — SGP4/SDP4 orbital propagation library
- **NumPy** — Numerical computation for orbital mechanics
- **IBM watsonx-ai** — IBM Granite model integration
- **httpx** — Async HTTP client for CelesTrak API

### Frontend
- **Next.js 14** — React framework with App Router
- **TypeScript** — Type-safe development
- **Tailwind CSS** — Utility-first styling (dark mission-control theme)
- **CesiumJS** — 3D globe visualization
- **Lucide React** — Icon library

### Data Sources
- **CelesTrak** — Live Two-Line Element (TLE) orbital data
- **Space-Track.org** — Conjunction Data Messages (CDMs)

### AI
- **IBM Granite** (via watsonx) — Decision intelligence and operator briefing generation
- **IBM Bob** — Primary development tool

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- IBM watsonx API key (optional — demo mode works without it)

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your watsonx credentials (or leave DEMO_MODE=true)
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the AstraGuard dashboard.

---

## 📹 Demo Video

[Watch the 3-minute demo →](#) *(link to be added)*

### Demo Walkthrough
1. **0:00** — AstraGuard dashboard loads with 3D orbital display showing tracked satellites and debris
2. **0:20** — Conjunction alert fires: ISS vs Cosmos-2251 debris at 1.8 km miss distance
3. **0:40** — Countdown timer shows time to closest approach
4. **1:00** — Operator clicks "Analyze" — system generates three avoidance maneuvers
5. **1:30** — IBM Granite AI recommends the Balanced maneuver with detailed reasoning
6. **2:00** — Operator reviews trade-off analysis and risk factors
7. **2:20** — Operator approves the maneuver — trajectory updates on the globe
8. **2:50** — "Physics calculates. AI decides. Operators approve."

---

## 📁 Project Structure

```
astraguard/
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI application
│   │   ├── models.py             # Pydantic data models
│   │   ├── tle_fetcher.py        # CelesTrak TLE data fetcher
│   │   ├── orbit_propagator.py   # SGP4 orbital propagation engine
│   │   ├── conjunction_detector.py # Close approach detection
│   │   ├── risk_scorer.py        # Multi-factor risk assessment
│   │   ├── maneuver_generator.py # Avoidance maneuver calculator
│   │   └── granite_advisor.py    # IBM Granite AI integration
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/                  # Next.js App Router pages
│   │   ├── components/           # React components
│   │   │   ├── CesiumGlobe.tsx   # 3D orbital visualization
│   │   │   ├── Dashboard.tsx     # Main dashboard container
│   │   │   ├── ConjunctionAlert.tsx
│   │   │   ├── ManeuverPanel.tsx
│   │   │   ├── AIAdvisorPanel.tsx
│   │   │   ├── RiskGauge.tsx
│   │   │   └── StatsBar.tsx
│   │   └── lib/
│   │       ├── api.ts            # Backend API client
│   │       └── types.ts          # TypeScript interfaces
│   └── package.json
├── README.md
└── .gitignore
```

---

## 👥 Team

- [Your Name] — Developer

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.
