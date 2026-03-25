# src/gtm_crew/crew.py
# Defines the GTM Strategy Crew: agents, tasks, and crew assembly.
# Tasks are loaded from tasks.yaml; the final task outputs a GTMBlueprint Pydantic object.

from typing import List, Any
import yaml
import os
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from gtm_crew.models.gtm_plan_models import GTMBlueprint
from crewai_tools import FileReadTool, SerperDevTool
from dotenv import load_dotenv
load_dotenv()


@CrewBase
class GTMStrategyCrew:
    """GTM Strategy Crew for SaaS/AI products."""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        # Load tasks.yaml manually so task descriptions can reference
        # pattern file content and input variables at runtime.
        config_path = os.path.join(os.path.dirname(__file__), "config", "tasks.yaml")
        with open(config_path, "r", encoding="utf-8") as f:
            self._tasks_cfg: dict[str, Any] = yaml.safe_load(f)

        # FileReadTools for pattern files used by channel, metrics, and risk agents.
        patterns_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patterns")
        self.channels_tool = FileReadTool(file_path=os.path.join(patterns_dir, "gtm_channels.md"))
        self.metrics_tool  = FileReadTool(file_path=os.path.join(patterns_dir, "saas_metrics.md"))
        self.risks_tool    = FileReadTool(file_path=os.path.join(patterns_dir, "gtm_risks.md"))


    # -- Agents ---------------------------------------------------------------

    @agent
    def market_research_analyst(self) -> Agent:
        # Researches competitors, market size, trends, and buyer pains.
        return Agent(
            role="Market Research Analyst",
            goal="Understand the market, competitors, and buyer pains for SaaS/AI products.",
            backstory=(
                "Expert at finding SaaS/AI competitors, analyzing websites, "
                "and summarizing trends for founders with limited GTM experience."
            ),
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def icp_persona_designer(self) -> Agent:
        # Defines the ideal customer profile and 2-3 buyer personas from research output.
        return Agent(
            role="ICP & Persona Designer",
            goal="Define a clear ICP and 1-3 buyer personas using research and user input.",
            backstory=(
                "Helps B2B SaaS teams clarify target buyers, their pains, goals, "
                "and objections, especially at MVP/early-revenue stage."
            ),
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def positioning_strategist(self) -> Agent:
        # Crafts positioning statement, value propositions, and persona-specific messaging.
        return Agent(
            role="Positioning & Messaging Strategist",
            goal="Craft positioning, value propositions, and key messages aligned with ICP and personas.",
            backstory=(
                "Former B2B SaaS marketer who writes clear, differentiated positioning "
                "and persona-specific messaging."
            ),
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def channel_planner(self) -> Agent:
        # Selects GTM channels and designs ICE-scored experiments within budget and team constraints.
        # Uses SerperDevTool for live channel data and channels_tool for reach benchmarks.
        return Agent(
            role="Channel & Experiment Planner",
            goal="Select channels and design experiments that fit stage, budget, and team size.",
            backstory=(
                "Experienced early-stage SaaS GTM operator skilled at low-budget, "
                "high-learning experiments across outbound, content, and communities."
            ),
            tools=[SerperDevTool(), self.channels_tool],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def metrics_risk_analyst(self) -> Agent:
        # Defines the North Star metric, KPIs, funnel stages, and risk register.
        # Uses pattern files for SaaS benchmark data and common GTM risk patterns.
        return Agent(
            role="Metrics & Risk Analyst",
            goal="Define GTM KPIs, funnel metrics, and key risks with mitigations.",
            backstory=(
                "Data-driven marketer who builds simple funnels and surfaces "
                "assumptions and risks for new GTM motions."
            ),
            tools=[self.metrics_tool, self.risks_tool],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def gtm_orchestrator(self) -> Agent:
        # Final quality-gate agent that integrates all prior outputs into one
        # consistent GTMBlueprint and runs all consistency checks.
        return Agent(
            role="GTM Orchestrator (CMO/PM)",
            goal="Integrate all sections into a coherent, constraint-aware GTM blueprint.",
            backstory=(
                "Senior PM/CMO who coordinates cross-functional GTM efforts and "
                "ensures recommendations fit budget, stage, and team capacity."
            ),
            verbose=True,
            allow_delegation=False,
        )


    # -- Tasks ----------------------------------------------------------------
    # Each task loads its description and expected_output from tasks.yaml.
    # Input variables (e.g. {product_description}) are interpolated by CrewAI
    # at kickoff time using the inputs dict passed to crew().kickoff().

    @task
    def market_research_task(self) -> Task:
        cfg = self._tasks_cfg["market_research_task"]
        return Task(
            description=cfg["description"],
            expected_output=cfg["expected_output"],
            agent=self.market_research_analyst(),
        )

    @task
    def icp_persona_task(self) -> Task:
        cfg = self._tasks_cfg["icp_persona_task"]
        return Task(
            description=cfg["description"],
            expected_output=cfg["expected_output"],
            agent=self.icp_persona_designer(),
        )

    @task
    def positioning_task(self) -> Task:
        cfg = self._tasks_cfg["positioning_task"]
        return Task(
            description=cfg["description"],
            expected_output=cfg["expected_output"],
            agent=self.positioning_strategist(),
        )

    @task
    def channel_plan_task(self) -> Task:
        cfg = self._tasks_cfg["channel_plan_task"]
        return Task(
            description=cfg["description"],
            expected_output=cfg["expected_output"],
            agent=self.channel_planner(),
        )

    @task
    def metrics_risk_task(self) -> Task:
        cfg = self._tasks_cfg["metrics_risk_task"]
        return Task(
            description=cfg["description"],
            expected_output=cfg["expected_output"],
            agent=self.metrics_risk_analyst(),
        )

    @task
    def final_blueprint_task(self) -> Task:
        # output_pydantic forces the orchestrator to return a validated GTMBlueprint object.
        cfg = self._tasks_cfg["final_blueprint_task"]
        return Task(
            description=cfg["description"],
            expected_output=cfg["expected_output"],
            agent=self.gtm_orchestrator(),
            output_pydantic=GTMBlueprint,
        )


    # -- Crew -----------------------------------------------------------------

    @crew
    def crew(self) -> Crew:
        # Sequential process: each task receives the accumulated context
        # from all prior tasks before executing.
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
