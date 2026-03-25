# src/gtm_crew/main.py
# CLI entry point for the GTM Strategy Crew.
# Used when running the crew directly via terminal instead of the Streamlit app.

from dotenv import load_dotenv
load_dotenv()

from typing import Literal, cast
from .crew import GTMStrategyCrew
from gtm_crew.models.gtm_plan_models import GTMBlueprint
from gtm_crew.models.input_models import GTMInput


def run():
    print("GTM Strategy Crew - CLI Mode")
    print("-" * 40)

    # Collect Literal-typed fields first so cast() can satisfy Pylance.
    # Pydantic will validate the actual values at GTMInput construction time.
    stage_input = input("Stage [idea / MVP / early-revenue / growth] (default: MVP): ").strip() or "MVP"
    pricing_input = input("Pricing model [subscription / usage-based / freemium / one-time] (default: subscription): ").strip() or "subscription"
    budget_input = input("Budget level [low / medium / high] (default: low): ").strip() or "low"

    gtm_input = GTMInput(
        product_description=input("Product description: ").strip(),
        target_audience=input("Target audience: ").strip(),
        stage=cast(Literal["idea", "MVP", "early-revenue", "growth"], stage_input),
        pricing_model=cast(Literal["subscription", "usage-based", "freemium", "one-time"], pricing_input),
        budget_level=cast(Literal["low", "medium", "high"], budget_input),
        timeline_weeks=int(input("Timeline in weeks (default: 8): ").strip() or 8),
        team_size=input("Team size (default: solo + 1 engineer): ").strip() or "solo + 1 engineer",
    )

    print("\nRunning GTM Strategy Crew...\n")

    result = GTMStrategyCrew().crew().kickoff(inputs=gtm_input.model_dump())
    blueprint: GTMBlueprint = result.pydantic

    if blueprint:
        # Print a summary; full output is available via PDF/JSON export in the app.
        print("\nStructured GTM Blueprint generated!")
        print(f"Product : {blueprint.product_name}")
        print(f"Stage   : {blueprint.stage}")
        print("\nNext Steps (7-day checklist):")
        for i, step in enumerate(blueprint.next_steps, 1):
            print(f"  {i}. {step}")
    else:
        # Crew completed but output did not parse into GTMBlueprint.
        print("\nPydantic parsing failed - raw output:")
        print(result.raw)


if __name__ == "__main__":
    run()
