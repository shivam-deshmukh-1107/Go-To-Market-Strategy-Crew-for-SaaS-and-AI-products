# Go-To-Market Strategy Crew for SaaS & AI Products

An agentic AI application that generates a complete **Go-To-Market (GTM) blueprint** for SaaS and AI products using **CrewAI**, **Streamlit**, and **Pydantic**. It helps founders, solo builders, and early-stage teams convert a product idea plus business constraints into a structured GTM strategy with market research, ICP, personas, positioning, channels, experiments, KPIs, risks, and a week-by-week action plan.

---

## Overview

Launching a SaaS or AI product requires much more than building a working product. Teams must identify the right customer, understand market dynamics, differentiate against competitors, choose practical acquisition channels, and execute within real constraints such as budget, timeline, and team size.[file:51]

This project solves that problem by building a multi-agent GTM planning system that acts like a virtual strategy team. The app accepts a short product description and business inputs, runs a CrewAI workflow, and generates a structured GTM blueprint that can be viewed in the browser and exported as PDF or JSON.[file:51][file:52][file:58]

---

## Problem Statement

Many founders and small teams struggle with GTM planning because they:[file:51]

- Do not have dedicated GTM or marketing experts.
- Spend too much time manually researching competitors and defining ICPs.
- Create plans that are incomplete, unstructured, or misaligned with budget and execution capacity.

This project addresses that gap by creating a practical, reusable GTM generation workflow for SaaS and AI products.[file:51]

---

## Project Goal

The goal of this project is to build a **multi-agent GTM Strategy Crew** that:[file:51]

- Accepts a short product description and business constraints as input.
- Produces a structured, realistic GTM blueprint.
- Supports SaaS and AI product use cases.
- Demonstrates how agentic AI can be applied to real business workflows.

---

## What the App Generates

The system generates a GTM blueprint with the following sections:[file:51][file:52][file:58][file:59]

- Product and problem summary
- Market context and key trends
- Competitive landscape
- Differentiation hints
- Ideal Customer Profile (ICP)
- 1 to 3 buyer personas
- Positioning statement
- Core value propositions
- Persona-specific messaging
- Primary channels
- Prioritized GTM experiments
- KPIs and funnel metrics
- GTM risks and mitigations
- Week-by-week action plan
- 7-day founder checklist

---

## Features

- Multi-agent GTM workflow powered by CrewAI.[file:51][file:53]
- Streamlit-based user interface for structured GTM input collection.[file:52]
- Pydantic-based structured input and output models.[file:52][file:53][file:54]
- Strategy generation tailored to budget, timeline, stage, and team size.[file:51][file:52]
- Interactive blueprint display across multiple UI tabs.[file:59]
- Export to **PDF** for shareable reports.[file:52][file:58]
- Export to **JSON** for structured storage or downstream integrations.[file:52]
- Clear separation of orchestration, models, and UI rendering.[file:53][file:58][file:59]

---

## Multi-Agent Architecture

This project uses a six-agent CrewAI workflow running in a **sequential process**. Each agent is responsible for one GTM layer, and the final orchestrator consolidates all sections into one coherent blueprint.[file:51][file:53]

### Agents

1. **Market Research Analyst**  
   Understands the market, competitors, buyer pain points, and broader category context.[file:51][file:53]

2. **ICP Persona Designer**  
   Defines the Ideal Customer Profile and creates detailed buyer personas.[file:51][file:53]

3. **Positioning & Messaging Strategist**  
   Crafts the positioning statement, value propositions, and persona-specific messaging.[file:51][file:53]

4. **Channel Experiment Planner**  
   Selects acquisition channels and designs experiments that fit the product stage, budget, and team size.[file:51][file:53]

5. **Metrics & Risk Analyst**  
   Defines success metrics, funnel stages, and key GTM risks with mitigations.[file:51][file:53]

6. **GTM Orchestrator (CMO/PM)**  
   Integrates all outputs into a consistent, constraint-aware GTM blueprint.[file:51][file:53]

---

## Workflow

The system works in the following sequence:[file:51][file:52][file:53][file:54]

1. The user enters product and business details in the Streamlit sidebar.
2. The app validates and structures the input using Pydantic models.
3. The CrewAI workflow runs multiple GTM tasks in sequence.
4. The final response is parsed into a structured `GTMBlueprint`.
5. The blueprint is rendered in the app and made available for PDF and JSON export.

---

## Input Fields

The Streamlit app currently collects the following inputs from the user:[file:52]

- **Product Description**
- **Target Audience**
- **Product Stage** — `idea`, `MVP`, `early-revenue`, `growth`
- **Pricing Model** — `subscription`, `usage-based`, `freemium`, `one-time`
- **Budget Level** — `low`, `medium`, `high`
- **Timeline (weeks)** — configurable from 4 to 52 weeks
- **Team Size**

These inputs are passed into the CrewAI workflow and used to tailor the generated strategy.[file:52][file:54]

---

## Output Sections

The generated GTM blueprint is displayed in the Streamlit UI with separate tabs for:[file:59]

- Market
- ICP & Personas
- Positioning
- Channels
- Metrics & Risks
- Action Plan
- Next Steps

The app also allows users to export the output in two formats:[file:52][file:58]

- **PDF Export** — formatted report for sharing and presentation
- **JSON Export** — structured machine-readable output

---

## Tech Stack

This project uses the following technologies:[file:51][file:52][file:53][file:58]

- **Python**
- **CrewAI**
- **Streamlit**
- **Pydantic**
- **FPDF**
- **PyYAML**
- **python-dotenv**

---

## Sample GTM Blueprint Output

To see what the GTM Strategy Crew produces end‑to‑end, you can download a full example generated for an AI-powered support analytics product called **InsightPulse**.

- 📄 **Sample GTM Blueprint (PDF)**  
  [Download InsightPulse GTM Blueprint (PDF)](GTM_Blueprint_InsightPulse.pdf)

- 🧾 **Sample GTM Blueprint (JSON)**  
  [Download InsightPulse GTM Blueprint (JSON)](GTM_Blueprint_InsightPulse.json)


---

## Project Structure

```bash
.
├── app.py
├── src/
│   └── gtmcrew/
│       ├── crew.py
│       ├── main.py
│       ├── models/
│       │   ├── input_models.py
│       │   └── gtm_plan_models.py
│       └── ui/
│           ├── components.py
│           └── pdf_export.py
├── config/
│   └── tasks.yaml
└── README.md
