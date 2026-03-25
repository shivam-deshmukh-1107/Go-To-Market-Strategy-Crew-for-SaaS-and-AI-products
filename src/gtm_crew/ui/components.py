# src/gtm_crew/ui/components.py
# Streamlit rendering functions for each section of the GTMBlueprint.
# Each function takes the full blueprint and renders one section.
# render_blueprint() is the top-level entry point used by app.py.

import streamlit as st
from gtm_crew.models.gtm_plan_models import GTMBlueprint


def render_market_research(bp: GTMBlueprint):
    st.subheader("🔍 Market Research")
    st.write(bp.market_research.market_summary)

    st.markdown("**Key Trends**")
    for trend in bp.market_research.key_trends:
        st.markdown(f"- {trend}")

    # Competitor table: one row per competitor with core attributes.
    st.markdown("**Competitive Landscape**")
    rows = [
        {
            "Competitor": c.name,
            "Target Segment": c.target_segment,
            "Key Features": c.key_features,
            "Pricing": c.pricing_positioning,
            "Differentiation": c.differentiation_notes,
        }
        for c in bp.market_research.competitors
    ]
    st.dataframe(rows, width='stretch')

    st.markdown("**Differentiation Hints for Your Product**")
    for hint in bp.market_research.differentiation_hints:
        st.markdown(f"- {hint}")


def render_icp_personas(bp: GTMBlueprint):
    st.subheader("🎯 ICP & Buyer Personas")

    # ICP summary split across two columns for readability.
    icp = bp.icp_and_personas.icp
    with st.expander("Ideal Customer Profile (ICP)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Company Size:** {icp.company_size}")
            st.markdown(f"**Budget Level:** {icp.budget_level}")
            st.markdown("**Industries:**")
            for i in icp.industries:
                st.markdown(f"  - {i}")
        with col2:
            st.markdown("**Geography:**")
            for g in icp.geography:
                st.markdown(f"  - {g}")
            st.markdown("**Tech Stack:**")
            for t in icp.tech_stack:
                st.markdown(f"  - {t}")

    # One expander per persona; pains/goals on the left, triggers/objections on the right.
    for persona in bp.icp_and_personas.personas:
        with st.expander(f"👤 {persona.name} — {persona.role}"):
            st.markdown(f"**Responsibilities:** {persona.responsibilities}")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Pains:**")
                for p in persona.pains:
                    st.markdown(f"- {p}")
                st.markdown("**Goals:**")
                for g in persona.goals:
                    st.markdown(f"- {g}")
            with col2:
                st.markdown("**Buying Triggers:**")
                for t in persona.buying_triggers:
                    st.markdown(f"- {t}")
                st.markdown("**Objections:**")
                for o in persona.objections:
                    st.markdown(f"- {o}")
            st.success(f"Success Criteria: {persona.success_criteria}")


def render_positioning(bp: GTMBlueprint):
    st.subheader("💬 Positioning & Messaging")

    st.info(f"**Positioning Statement:**\n\n{bp.positioning.positioning_statement}")

    st.markdown("**Value Propositions**")
    for i, vp in enumerate(bp.positioning.value_propositions, 1):
        st.markdown(f"**{i}.** {vp}")

    # One expander per persona showing headline and supporting bullets.
    st.markdown("**Persona-Specific Messages**")
    for pm in bp.positioning.persona_messages:
        with st.expander(f"📣 {pm.persona_name}"):
            st.markdown(f"**Headline:** {pm.headline}")
            for bullet in pm.key_bullets:
                st.markdown(f"- {bullet}")


def render_channel_plan(bp: GTMBlueprint):
    st.subheader("📡 Channel & Experiment Strategy")

    # Each channel in its own expander showing rationale.
    st.markdown("**Primary Channels**")
    for ch in bp.channel_plan.primary_channels:
        with st.expander(f"📌 {ch.name} — Effort: `{ch.effort}`"):
            st.write(ch.rationale)

    # Experiment summary table; full details are in the PDF export.
    st.markdown("**Prioritized Experiments**")
    rows = [
        {
            "Experiment": e.name,
            "Goal": e.goal,
            "Effort": e.effort,
            "Timing": e.timing,
            "Success Metric": e.success_metric,
        }
        for e in bp.channel_plan.experiments
    ]
    st.dataframe(rows, width='stretch')


def render_metrics_risks(bp: GTMBlueprint):
    st.subheader("📊 Metrics & Risks")

    st.markdown("**Primary KPIs**")
    for kpi in bp.metrics_and_risks.primary_kpis:
        st.markdown(f"- {kpi}")

    # Each funnel stage in its own expander with description and example metric.
    st.markdown("**GTM Funnel**")
    for stage in bp.metrics_and_risks.funnel:
        with st.expander(f"🔹 {stage.stage}"):
            st.write(stage.description)
            st.markdown(f"*Example metric: {stage.example_metric}*")

    st.markdown("**Risk Table**")
    rows = [
        {
            "Risk": r.risk,
            "Impact": r.impact,
            "Likelihood": r.likelihood,
            "Mitigation": r.mitigation,
        }
        for r in bp.metrics_and_risks.risks
    ]
    st.dataframe(rows, width='stretch')


def render_action_plan(bp: GTMBlueprint):
    st.subheader(f"🗓️ {bp.action_plan.timeline_weeks}-Week GTM Action Plan")
    # One expander per week showing the focus area and individual actions.
    for wa in bp.action_plan.weekly_actions:
        with st.expander(f"Week {wa.week} — {wa.focus}"):
            for action in wa.actions:
                st.markdown(f"- {action}")


def render_next_steps(bp: GTMBlueprint):
    # Interactive checkboxes let the founder tick off each day-1 action.
    st.subheader("✅ Next Steps — 7-Day Founder Checklist")
    for i, step in enumerate(bp.next_steps, 1):
        st.checkbox(step, key=f"next_step_{i}")


def render_blueprint(bp: GTMBlueprint):
    """Render all blueprint sections as labelled tabs."""
    tabs = st.tabs([
        "🔍 Market",
        "🎯 ICP & Personas",
        "💬 Positioning",
        "📡 Channels",
        "📊 Metrics & Risks",
        "🗓️ Action Plan",
        "✅ Next Steps",
    ])

    with tabs[0]: render_market_research(bp)
    with tabs[1]: render_icp_personas(bp)
    with tabs[2]: render_positioning(bp)
    with tabs[3]: render_channel_plan(bp)
    with tabs[4]: render_metrics_risks(bp)
    with tabs[5]: render_action_plan(bp)
    with tabs[6]: render_next_steps(bp)
