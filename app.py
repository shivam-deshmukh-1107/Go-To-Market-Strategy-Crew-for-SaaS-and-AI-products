# app.py
# Streamlit entry point for the GTM Strategy Crew web application.
# Handles page config, session state, input form, crew execution, and blueprint rendering.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from gtm_crew.models.input_models import GTMInput
from gtm_crew.models.gtm_plan_models import GTMBlueprint
from gtm_crew.crew import GTMStrategyCrew
from gtm_crew.ui.components import render_blueprint
from gtm_crew.ui.pdf_export import generate_pdf


st.set_page_config(
    page_title="GTM Strategy Crew",
    page_icon="🚀",
    layout="wide",
)

# Reduce default top/bottom padding added by Streamlit's block container.
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize blueprint in session state on first load.
if "blueprint" not in st.session_state:
    st.session_state.blueprint = None


# -- Sidebar ------------------------------------------------------------------
# Shows feature overview before generation; switches to export controls after.
with st.sidebar:
    st.title("🚀 GTM Strategy Crew")
    st.caption("AI-powered Go-To-Market blueprints for SaaS products.")
    st.divider()

    if st.session_state.blueprint is None:
        # Feature list shown before the user generates a blueprint.
        st.markdown("#### 🤖 What Gets Generated")
        st.markdown("""
            <div style='font-size: 0.82rem; line-height: 1.7; color: #ccc'>

            🔍 &nbsp;<b>Market Research</b><br>
            <span style='color:#999; padding-left: 18px; display:block'>TAM, trends, competitors with pricing tiers & exploitable gaps</span>

            🎯 &nbsp;<b>ICP & Buyer Personas</b><br>
            <span style='color:#999; padding-left: 18px; display:block'>3 quantified personas with pains, goals, tools & success criteria</span>

            💬 &nbsp;<b>Positioning & Messaging</b><br>
            <span style='color:#999; padding-left: 18px; display:block'>Positioning statement + persona-specific headlines & value props</span>

            📡 &nbsp;<b>Channel & Experiment Plan</b><br>
            <span style='color:#999; padding-left: 18px; display:block'>Channels with reach estimates + ICE-scored sequenced experiments</span>

            📊 &nbsp;<b>Metrics & Risks</b><br>
            <span style='color:#999; padding-left: 18px; display:block'>North Star KPI, 5 tracked KPIs, GTM funnel, 7 risks with owners</span>

            🗓️ &nbsp;<b>Action Plan</b><br>
            <span style='color:#999; padding-left: 18px; display:block'>Week-by-week execution plan + 7-day founder checklist with tools</span>

            </div>
        """, unsafe_allow_html=True)

    else:
        # Post-generation: show product name, export buttons, and reset option.
        bp = st.session_state.blueprint
        st.markdown(f"#### 📄 {bp.product_name}")
        st.caption(f"Stage: **{bp.stage}**")
        st.divider()

        # Export blueprint as PDF.
        pdf_buffer = generate_pdf(bp)
        st.download_button(
            label="📥 Export PDF",
            data=pdf_buffer,
            file_name=f"GTM_Blueprint_{bp.product_name.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

        st.markdown("<div style='margin-top:6px'></div>", unsafe_allow_html=True)

        # Export blueprint as JSON.
        json_export = bp.model_dump_json(indent=2)
        st.download_button(
            label="📋 Export JSON",
            data=json_export,
            file_name=f"GTM_Blueprint_{bp.product_name.replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True,
        )

        st.divider()

        # Clear session state and return to the input form.
        if st.button("🔄 New Blueprint", use_container_width=True):
            st.session_state.blueprint = None
            st.rerun()


# -- Main Page ----------------------------------------------------------------
if st.session_state.blueprint is None:

    # Hero header shown above the input form.
    st.markdown("""
    <h1 style='font-size:2.4rem; font-weight:800; margin-bottom:0.2rem'>
        🚀 GTM Strategy Crew
    </h1>
    <p style='font-size:1.05rem; color:#888; margin-top:0; margin-bottom:1.5rem'>
        Describe your product. Get a complete, investor-ready Go-To-Market blueprint — powered by 6 specialized AI agents.
    </p>
    """, unsafe_allow_html=True)

    st.divider()

    # Input form — all fields are submitted together on button click.
    with st.form("gtm_form"):

        # Full-width fields: product description and target audience.
        product_description = st.text_area(
            "📝 Product Description",
            value="",
            placeholder="e.g. AI that analyzes support tickets for SaaS teams.",
            height=90,
            help="Describe what your product does, who it's for, and the core problem it solves.",
        )

        target_audience = st.text_input(
            "👥 Target Audience",
            value="",
            placeholder="e.g. B2B SaaS product and support teams",
            help="Who are the primary buyers and users of this product?",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Compact row: stage, pricing model, budget, and team size side by side.
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            stage = st.selectbox(
                "🏁 Product Stage",
                options=["idea", "MVP", "early-revenue", "growth"],
                index=0,
                help="What stage is your product at?",
            )
        with c2:
            pricing_model = st.selectbox(
                "💳 Pricing Model",
                options=["subscription", "usage-based", "freemium", "one-time"],
                index=0,
            )
        with c3:
            budget_level = st.selectbox(
                "💰 GTM Budget",
                options=["low", "medium", "high"],
                index=0,
                help="Low = founder-led, no paid ads. Medium = some budget. High = full team + ads.",
            )
        with c4:
            team_size = st.text_input(
                "🧑‍💻 Team Size",
                value="",
                placeholder="e.g. solo founder, 2-person team",
                help="Who will execute this GTM? e.g. 'solo', '2-person team', '3-person founding team'",
            )

        # Full-width timeline slider.
        st.markdown("<br>", unsafe_allow_html=True)
        timeline_weeks = st.slider(
            "📅 GTM Timeline (weeks)",
            min_value=4,
            max_value=52,
            value=8,
            step=2,
            help="How many weeks should the action plan span?",
        )

        st.markdown("<br>", unsafe_allow_html=True)
        run_button = st.form_submit_button(
            "⚡ Generate GTM Blueprint",
            use_container_width=True,
            type="primary",
        )

    # Validate required fields after submit; run crew only if all are present.
    if run_button:
        if not product_description.strip() or not target_audience.strip() or not team_size.strip():
            st.warning("Please fill in Product Description, Target Audience, and Team Size before generating.")
        else:
            gtm_input = GTMInput(
                product_description=product_description,
                target_audience=target_audience,
                stage=stage,
                pricing_model=pricing_model,
                budget_level=budget_level,
                timeline_weeks=timeline_weeks,
                team_size=team_size,
            )
            with st.spinner("Running GTM Strategy Crew... this takes ~2 minutes"):
                try:
                    result = GTMStrategyCrew().crew().kickoff(
                        inputs=gtm_input.model_dump()
                    )
                    blueprint: GTMBlueprint = result.pydantic
                    if blueprint:
                        st.session_state.blueprint = blueprint
                        st.rerun()
                    else:
                        # Crew ran but output could not be parsed into GTMBlueprint.
                        st.error("Pydantic parsing failed. Raw output below:")
                        st.code(result.raw)
                except Exception as e:
                    st.error(f"Error: {e}")

else:
    # -- Blueprint Results View ------------------------------------------------
    # Rendered after a successful crew run; sidebar handles exports from here.
    bp = st.session_state.blueprint

    st.markdown(f"""
    <h1 style='font-size:2.2rem; font-weight:800; margin-bottom:0.2rem'>
        🚀 GTM Blueprint — {bp.product_name}
    </h1>
    <p style='color:#888; font-size:0.95rem; margin:0'>
        Stage: <strong>{bp.stage}</strong>
        &nbsp;·&nbsp;
        Use the sidebar to export your blueprint as PDF or JSON.
    </p>
    """, unsafe_allow_html=True)

    st.divider()
    render_blueprint(bp)
