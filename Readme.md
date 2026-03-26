# Go-To-Market Strategy Crew for SaaS & AI Products Using CrewAI

An multi-agentic AI application that generates a complete Go-To-Market (GTM) blueprint for SaaS and AI products using CrewAI, Streamlit, and Pydantic. It acts like a virtual strategy team for founders, solo builders, and early-stage teams who often lack dedicated GTM expertise, spend too much time on manual research, and end up with unstructured or unrealistic plans. By taking a short product description plus key business constraints (budget, timeline, team size, stage), it produces a structured GTM strategy covering market research, ICP and personas, positioning, channels, experiments, KPIs, risks, and a week‑by‑week action plan that can be reviewed in the browser and exported as PDF or JSON.

<img width="1842" height="926" alt="Project_UI" src="https://github.com/user-attachments/assets/f55f1d48-ca8e-44fc-9e80-85720f806ddb" />

---

## What the App Generates
The system produces a complete GTM blueprint that includes:

- Product and problem summary
- Market context, key trends, and competitive landscape
- Differentiation opportunities and positioning statement
- Ideal Customer Profile (ICP) and 1–3 detailed buyer personas
- Core value propositions and persona-specific messaging
- Recommended primary channels with rationale
- Prioritized GTM experiments with goals and timing
- KPIs, funnel metrics, and GTM risk analysis with mitigations
- Week-by-week GTM action plan
- 7-day, high‑impact founder execution checklist

## Features

- Multi-agent GTM workflow powered by CrewAI.
- Streamlit-based user interface for structured GTM input collection.
- Pydantic-based structured input and output models.
- Strategy generation tailored to budget, timeline, stage, and team size.
- Interactive blueprint display across multiple UI tabs.
- Export to **PDF** for shareable reports.
- Export to **JSON** for structured storage or downstream integrations.
- Clear separation of orchestration, models, and UI rendering.

## Generated GTM Stategy View:
<img width="1853" height="903" alt="Project_UI_Results" src="https://github.com/user-attachments/assets/09d26f0c-3c12-4114-a5f6-a79fab84477d" />

---

## Multi-Agent Architecture & Inputs
The app uses a **six‑agent, sequential CrewAI workflow**, where each agent owns one GTM layer and a final orchestrator merges everything into a single, coherent blueprint.

### Agents

- **Market Research Analyst** – Analyzes market context, competitors, and buyer pain points.  
- **ICP Persona Designer** – Defines the Ideal Customer Profile and creates detailed buyer personas.  
- **Positioning & Messaging Strategist** – Crafts the positioning statement, core value propositions, and persona‑specific messaging.  
- **Channel Experiment Planner** – Selects acquisition channels and designs GTM experiments aligned with stage, budget, and team size.  
- **Metrics & Risk Analyst** – Defines KPIs, funnel stages, and key GTM risks with mitigations.  
- **GTM Orchestrator (CMO/PM)** – Integrates all agent outputs into a constraint‑aware GTM blueprint.

### Input Fields (from the Streamlit app)

- **Product Description** – What the product does and the problem it solves.  
- **Target Audience** – Who the product is for (e.g., B2B SaaS product and support teams).  
- **Product Stage** – `idea`, `MVP`, `early-revenue`, or `growth`.  
- **Pricing Model** – `subscription`, `usage-based`, `freemium`, or `one-time`.  
- **Budget Level** – `low`, `medium`, or `high`.  
- **Timeline (weeks)** – Configurable range, typically 4–52 weeks.  
- **Team Size** – Brief description of the GTM team (e.g., “solo founder, 2‑person team”).  

These inputs are passed into the multi‑agent workflow so each agent tailors its recommendations to the product’s real constraints and context.


---

## Sample GTM Blueprint Output

To see what the GTM Strategy Crew produces end‑to‑end, you can download a full example generated for an AI-powered support analytics product called **InsightPulse**.

- 📄 **Sample GTM Blueprint (PDF)**  
  [Download InsightPulse GTM Blueprint (PDF)](GTM_Blueprint_InsightPulse.pdf)

- 🧾 **Sample GTM Blueprint (JSON)**  
  [Download InsightPulse GTM Blueprint (JSON)](GTM_Blueprint_InsightPulse.json)


---
