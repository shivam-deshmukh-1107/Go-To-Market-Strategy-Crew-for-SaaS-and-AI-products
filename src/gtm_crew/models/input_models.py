# src/gtm_crew/models/input_models.py
# Pydantic model for validating user-supplied GTM inputs before passing
# them to the crew via kickoff(inputs=gtm_input.model_dump()).

from pydantic import BaseModel, Field
from typing import Literal


class GTMInput(BaseModel):
    product_description: str = Field(
        description="Short description of the product and its core value."
    )
    target_audience: str = Field(
        description="Who the product is for — industry, role, or team type."
    )
    stage: Literal["idea", "MVP", "early-revenue", "growth"] = Field(
        default="MVP",
        description="Current stage of the product."
    )
    pricing_model: Literal["subscription", "usage-based", "freemium", "one-time"] = Field(
        default="subscription",
        description="How the product is priced."
    )
    budget_level: Literal["low", "medium", "high"] = Field(
        default="low",
        # Drives channel constraints: low = no paid ads, high = full spend allowed.
        description="Available GTM budget level."
    )
    timeline_weeks: int = Field(
        default=8,
        ge=4,
        le=52,
        # Used by tasks.yaml to scope the action plan and experiment sequencing.
        description="Number of weeks for the GTM plan."
    )
    team_size: str = Field(
        default="solo + 1 engineer",
        # Used to cap simultaneous active channels (max 3 for teams of 1-2).
        description="Who is executing the GTM plan."
    )
