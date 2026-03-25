# src/gtm_crew/models/gtm_plan_models.py
# Pydantic models for the full GTM blueprint output.
# Structured as one model per blueprint section, composed into GTMBlueprint.
# Used as output_pydantic on the final_blueprint_task in crew.py.

from pydantic import BaseModel, Field
from typing import List, Optional


# -- Section 1: Market Research -----------------------------------------------

class Competitor(BaseModel):
    name: str
    target_segment: str                    # specific company size + industry
    key_features: str                      # named features, not categories
    pricing_positioning: str               # general pricing position
    pricing_tiers: Optional[str] = None    # e.g. "Starter - $15/mo, Pro - $49/mo"
    differentiation_notes: str             # observed weakness from customer perspective
    exploitable_gap: Optional[str] = None  # specific GTM attack angle against this competitor


class MarketResearch(BaseModel):
    market_summary: str                    # must include TAM + CAGR
    key_trends: List[str]                  # exactly 5, each citing a named company/stat from 2025-2026
    competitors: List[Competitor]          # 5-7 entries
    differentiation_hints: List[str]       # exactly 5, each referencing a distinct unmet need


# -- Section 2: ICP & Personas ------------------------------------------------

class ICP(BaseModel):
    company_size: str                      # headcount range + revenue range
    industries: List[str]                  # one item per industry, with sub-niche specified
    tech_stack: List[str]                  # one tool per list item, no sentences
    geography: List[str]                   # specific countries or metro regions
    budget_level: str                      # monthly spend range in USD


class BuyerPersona(BaseModel):
    name: str                              # job title at a specific company stage
    role: str
    company_stage: Optional[str] = None    # e.g. "Series A SaaS, 20-80 employees"
    day_in_the_life: Optional[str] = None  # current workflow without this product, naming the tool and pain
    responsibilities: str
    pains: List[str]                       # min 3, each must include a quantity or frequency
    goals: List[str]                       # each tied to a measurable outcome and timeframe
    buying_triggers: List[str]             # specific named events, not general pressures
    objections: List[str]                  # each must reference a named competitor or tool
    success_criteria: str                  # metric + baseline value + target value + timeframe
    current_tools: Optional[List[str]] = None  # tools the persona uses today


class ICPAndPersonas(BaseModel):
    icp: ICP
    personas: List[BuyerPersona]           # 2-3 personas covering the full decision-making unit


# -- Section 3: Positioning & Messaging ---------------------------------------

class PersonaMessage(BaseModel):
    persona_name: str
    headline: str                          # max 12 words, tone matched to persona archetype
    key_bullets: List[str]                 # exactly 3-4, each referencing a specific feature and outcome


class Positioning(BaseModel):
    positioning_statement: str             # follows "For X who Y, unlike Z, we W" template
    value_propositions: List[str]          # exactly 3, each naming a persona and including an outcome metric
    persona_messages: List[PersonaMessage]


# -- Section 4: Channel & Experiment Strategy ---------------------------------

class Channel(BaseModel):
    name: str
    rationale: str                         # why this channel fits this product and persona at this stage
    effort: str                            # low / medium / high
    target_persona: Optional[str] = None   # persona this channel primarily reaches
    monthly_reach: Optional[str] = None    # numeric reach with units and context, from gtm_channels.md
    first_action: Optional[str] = None     # single concrete action executable this week


class Experiment(BaseModel):
    name: str
    goal: str
    description: str                       # specific execution steps
    effort: str                            # low / medium / high
    timing: str                            # specific week range e.g. "Weeks 1-3"
    baseline: Optional[str] = None         # current state before the experiment runs
    target: Optional[str] = None           # desired state after the experiment
    success_metric: str                    # what is measured and with which tool
    ice_score: Optional[int] = None        # sum of Impact + Confidence + Ease (range 3-30)
    depends_on: Optional[str] = None       # name of prior experiment this builds on, or "None"


class ChannelPlan(BaseModel):
    primary_channels: List[Channel]        # 3-5 channels, each with unique monthly_reach value
    experiments: List[Experiment]          # 4-6 experiments sequenced awareness -> engagement -> conversion


# -- Section 5: Metrics & Risks -----------------------------------------------

class KPI(BaseModel):
    name: str
    baseline: str                          # value at GTM start; use "0" if pre-launch
    target: str                            # value to reach by end of timeline_weeks
    measurement_tool: str                  # e.g. Mixpanel, HubSpot, Google Analytics, manual
    is_north_star: bool = False            # True for the single most important KPI only


class FunnelStage(BaseModel):
    stage: str                             # e.g. Awareness, Consideration, Conversion, Activation, Retention
    description: str                       # activities driving movement into this stage
    example_metric: str                    # specific number derived from prior stage * conversion_rate
    conversion_rate: Optional[str] = None  # rate to next stage; "N/A" on the final Retention stage


class Risk(BaseModel):
    risk: str                              # specific to this product, stage, and market
    impact: str                            # High / Medium / Low
    likelihood: str                        # High / Medium / Low
    mitigation: str                        # specific action with a named responsible role
    early_warning_signal: Optional[str] = None  # observable event with threshold and timeframe
    owner: Optional[str] = None            # role accountable for executing the mitigation


class MetricsAndRisks(BaseModel):
    north_star_metric: Optional[str] = None  # single metric that best captures GTM progress
    primary_kpis: List[KPI]                  # 4-5 KPIs including both leading and lagging indicators
    funnel: List[FunnelStage]                # 4-5 stages ending on Retention with consistent math
    risks: List[Risk]                        # 6-7 risks, at least 2 competitor-specific


# -- Section 6: Weekly Action Plan --------------------------------------------

class WeeklyAction(BaseModel):
    week: str                              # e.g. "1" or "1-2"
    focus: str
    actions: List[str]                     # 3 specific, assignable actions for this week


class ActionPlan(BaseModel):
    timeline_weeks: int
    weekly_actions: List[WeeklyAction]     # length must equal timeline_weeks


# -- Root: Full GTM Blueprint -------------------------------------------------

class GTMBlueprint(BaseModel):
    product_name: str
    stage: str
    market_research: MarketResearch
    icp_and_personas: ICPAndPersonas
    positioning: Positioning
    channel_plan: ChannelPlan
    metrics_and_risks: MetricsAndRisks
    action_plan: ActionPlan
    next_steps: List[str] = Field(
        description=(
            "Exactly 7 day-labeled, tool-specific, time-estimated actions "
            "for the founder to complete in the next 7 days. "
            "Format: 'Day X: [Action] using [Tool] — expected time: [Xh]'. "
            "Must NOT repeat the Week 1 action plan."
        )
    )
