# src/gtm_crew/ui/pdf_export.py
# Generates a multi-section PDF from a GTMBlueprint object using fpdf2.
# Returns a BytesIO buffer ready for Streamlit download or file write.

from fpdf import FPDF
from fpdf.enums import XPos, YPos
from io import BytesIO
from gtm_crew.models.gtm_plan_models import GTMBlueprint


def clean(text: str) -> str:
    """Normalize Unicode characters to latin-1 safe equivalents."""
    replacements = {
        '\u2014': '-',
        '\u2013': '-',
        '\u2018': "'",
        '\u2019': "'",
        '\u201c': '"',
        '\u201d': '"',
        '\u2022': '-',
        '\u2026': '...',
        '\u00e2\u0080\u0099': "'",
        '\xa0': ' ',
        '\u25cf': '-',
        '\u25a1': '[ ]',
        '\u2713': '[x]',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text.encode('latin-1', errors='replace').decode('latin-1')


def _safe_width(pdf: 'GTMBlueprintPDF', indent: float = 0) -> float:
    """Return usable cell width after margins and optional indent. Minimum 10mm."""
    remaining = pdf.w - pdf.r_margin - pdf.l_margin - indent
    return max(remaining, 10)


class GTMBlueprintPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(31, 119, 180)
        self.cell(0, 10, 'GTM Strategy Blueprint', border=0,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', border=0,
                  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')

    # -- Heading helpers ------------------------------------------------------

    def chapter_title(self, title):
        """Top-level section heading (blue, 14pt bold)."""
        self.set_font('Arial', 'B', 14)
        self.set_text_color(31, 119, 180)
        self.cell(0, 10, clean(title), border=0,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(2)

    def section_title(self, title):
        """Second-level heading (dark, 12pt bold)."""
        self.set_font('Arial', 'B', 12)
        self.set_text_color(44, 62, 80)
        self.cell(0, 8, clean(title), border=0,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(1)

    def subsection_title(self, title):
        """Third-level heading (dark grey, 11pt bold)."""
        self.set_font('Arial', 'B', 11)
        self.set_text_color(52, 73, 94)
        self.cell(0, 7, clean(title), border=0,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(1)

    # -- Text helpers ---------------------------------------------------------

    def body_text(self, text):
        """Standard paragraph text, reset to left margin before rendering."""
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.set_x(self.l_margin)
        self.multi_cell(_safe_width(self), 5, clean(text))
        self.ln(2)

    def bullet_point(self, text, symbol='-'):
        """Bullet item with a fixed 7mm symbol cell and wrapping text cell."""
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.set_x(self.l_margin)
        self.cell(7, 5, clean(symbol), border=0,
                  new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.multi_cell(_safe_width(self, indent=7), 5, clean(text))
        self.ln(0.5)

    def checkbox_item(self, text):
        """Checkbox item using [ ] with a 10mm prefix cell."""
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.set_x(self.l_margin)
        self.cell(10, 5, '[ ]', border=0,
                  new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.multi_cell(_safe_width(self, indent=10), 5, clean(text))
        self.ln(0.5)

    def label(self, text):
        """Bold inline label, no line break after."""
        self.set_font('Arial', 'B', 10)
        self.set_text_color(0, 0, 0)
        self.set_x(self.l_margin)
        self.cell(0, 5, clean(text), border=0,
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def small_text(self, text, indent=0):
        """9pt text with optional left indent via a leading invisible cell."""
        self.set_font('Arial', '', 9)
        self.set_text_color(0, 0, 0)
        self.set_x(self.l_margin)
        if indent > 0:
            self.cell(indent, 4, '', border=0,
                      new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.multi_cell(_safe_width(self, indent=indent), 4, clean(text))
        self.ln(0.5)

    def italic_text(self, text, indent=0):
        """9pt italic grey text with optional left indent."""
        self.set_font('Arial', 'I', 9)
        self.set_text_color(80, 80, 80)
        self.set_x(self.l_margin)
        if indent > 0:
            self.cell(indent, 4, '', border=0,
                      new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.multi_cell(_safe_width(self, indent=indent), 4, clean(text))
        self.ln(1)

    # -- Block helpers --------------------------------------------------------

    def info_box(self, text, bg_color=(240, 248, 255)):
        """Bordered, filled highlight box for key statements."""
        self.set_fill_color(*bg_color)
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.set_x(self.l_margin)
        self.multi_cell(_safe_width(self), 5, clean(text),
                        border=1, align='L', fill=True)
        self.ln(2)

    def horizontal_line(self):
        """Light grey divider line at the current Y position."""
        self.set_draw_color(200, 200, 200)
        self.line(self.l_margin, self.get_y(),
                  self.w - self.r_margin, self.get_y())
        self.ln(3)

    # -- Badge helpers --------------------------------------------------------

    def north_star_badge(self, text):
        """Gold 'NORTH STAR' label followed by the metric text."""
        self.set_x(self.l_margin)
        self.set_fill_color(255, 193, 7)
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', 'B', 8)
        self.cell(28, 5, 'NORTH STAR', border=0,
                  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)
        self.set_font('Arial', '', 9)
        self.set_fill_color(255, 248, 220)
        self.multi_cell(_safe_width(self, indent=28), 5, clean(f'  {text}'),
                        border=0, fill=True)
        self.ln(2)

    def ice_badge(self, score: int):
        """Color-coded ICE score badge: green >= 24, amber >= 15, grey below."""
        if score >= 24:
            color = (46, 204, 113)
        elif score >= 15:
            color = (230, 160, 0)
        else:
            color = (189, 195, 199)
        self.set_x(self.l_margin)
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 8)
        self.cell(22, 5, f'ICE: {score}', border=0,
                  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(6)

    def risk_badge(self, level):
        """Color-coded risk badge: red=HIGH, amber=MEDIUM, green=LOW."""
        level_upper = str(level).upper()
        if level_upper in ('HIGH', 'H'):
            color, text = (231, 76, 60), 'HIGH'
        elif level_upper in ('MEDIUM', 'M'):
            color, text = (230, 160, 0), 'MED'
        elif level_upper in ('LOW', 'L'):
            color, text = (46, 204, 113), 'LOW'
        else:
            color, text = (149, 165, 166), level_upper[:4]
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 8)
        self.cell(14, 5, text, border=0,
                  new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)
        self.set_text_color(0, 0, 0)
        self.cell(3, 5, '', border=0, new_x=XPos.RIGHT, new_y=YPos.TOP)

    # -- Structured row helpers -----------------------------------------------

    def kpi_row(self, kpi, is_north_star=False):
        """Renders a single KPI with name, baseline, target, and measurement tool."""
        self.set_x(self.l_margin)
        if is_north_star:
            self.set_fill_color(255, 248, 220)
            self.set_text_color(31, 119, 180)
        else:
            self.set_fill_color(245, 248, 255)
            self.set_text_color(44, 62, 80)
        self.set_font('Arial', 'B', 9)
        prefix = '* ' if is_north_star else '  '
        self.multi_cell(_safe_width(self), 5,
                        clean(f'{prefix}{kpi.name}'),
                        border=0, align='L', fill=True)
        self.set_font('Arial', '', 8)
        self.set_text_color(0, 0, 0)
        self.set_x(self.l_margin + 5)
        self.multi_cell(_safe_width(self, indent=5), 4,
                        clean(f'Baseline: {kpi.baseline}  ->  Target: {kpi.target}'
                              f'  |  Tool: {kpi.measurement_tool}'),
                        border=0, align='L')
        self.ln(1.5)

    def render_table_multiline(self, headers, rows, col_widths):
        """
        Wrapping table with alternating row fill and header repeat on page break.
        Column widths are scaled proportionally if they exceed available page width.
        """
        available = self.w - self.l_margin - self.r_margin
        total = sum(col_widths)
        if total > available:
            col_widths = [w * available / total for w in col_widths]

        line_h = 5

        def _draw_header():
            self.set_x(self.l_margin)
            self.set_font('Arial', 'B', 9)
            self.set_fill_color(31, 119, 180)
            self.set_text_color(255, 255, 255)
            for i, header in enumerate(headers):
                self.cell(col_widths[i], 7, clean(str(header)), border=1,
                          new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)
            self.ln()

        _draw_header()

        self.set_font('Arial', '', 8)
        self.set_text_color(0, 0, 0)

        for row_idx, row in enumerate(rows):
            fill = row_idx % 2 == 0
            self.set_fill_color(245, 245, 245) if fill \
                else self.set_fill_color(255, 255, 255)

            # Calculate the tallest cell in this row to set uniform row height.
            row_start_x = self.l_margin
            cell_heights = []
            for i, cell_text in enumerate(row):
                words = clean(str(cell_text)).split(' ')
                lines, current_line_w = 1, 0
                usable_w = col_widths[i] - 2
                for word in words:
                    word_w = self.get_string_width(word + ' ')
                    if current_line_w + word_w > usable_w and current_line_w > 0:
                        lines += 1
                        current_line_w = word_w
                    else:
                        current_line_w += word_w
                cell_heights.append(lines * line_h + 2)
            row_h = max(cell_heights)

            # Add a new page and redraw the header if this row would overflow.
            if self.get_y() + row_h > self.h - self.b_margin:
                self.add_page()
                _draw_header()
                self.set_font('Arial', '', 8)
                self.set_text_color(0, 0, 0)
                self.set_fill_color(245, 245, 245) if fill \
                    else self.set_fill_color(255, 255, 255)

            y_before = self.get_y()

            for i, cell_text in enumerate(row):
                cx = row_start_x + sum(col_widths[:i])
                self.set_xy(cx, y_before)
                self.set_fill_color(245, 245, 245) if fill \
                    else self.set_fill_color(255, 255, 255)
                self.rect(cx, y_before, col_widths[i], row_h, style='F')
                self.set_draw_color(180, 180, 180)
                self.rect(cx, y_before, col_widths[i], row_h, style='D')
                self.set_xy(cx + 1, y_before + 1)
                self.multi_cell(col_widths[i] - 2, line_h,
                                clean(str(cell_text)), border=0, align='L')

            self.set_xy(row_start_x, y_before + row_h)

        self.ln(3)


# -- PDF generation -----------------------------------------------------------

def generate_pdf(blueprint: GTMBlueprint) -> BytesIO:
    """Build and return the full GTM blueprint as a PDF byte stream."""
    pdf = GTMBlueprintPDF()
    pdf.add_page()

    # Cover page
    pdf.set_font('Arial', 'B', 22)
    pdf.set_text_color(31, 119, 180)
    pdf.cell(0, 20, 'GTM Blueprint', border=0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, clean(blueprint.product_name), border=0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f'Stage: {blueprint.stage}', border=0,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(10)

    # Section 1: Market Research
    pdf.add_page()
    pdf.chapter_title('1. Market Research')
    pdf.info_box(blueprint.market_research.market_summary)
    pdf.ln(2)

    pdf.section_title('Key Trends')
    for trend in blueprint.market_research.key_trends:
        pdf.bullet_point(trend)
    pdf.ln(3)

    pdf.section_title('Competitive Landscape')
    comp_headers = ['Competitor', 'Target Segment', 'Key Features',
                    'Pricing', 'Pricing Tiers']
    comp_rows = [
        [
            comp.name,
            comp.target_segment,
            comp.key_features,
            comp.pricing_positioning,
            comp.pricing_tiers or '-',
        ]
        for comp in blueprint.market_research.competitors
    ]
    pdf.render_table_multiline(comp_headers, comp_rows,
                               col_widths=[28, 35, 50, 35, 32])

    pdf.section_title('Competitive Differentiation Notes')
    for comp in blueprint.market_research.competitors:
        pdf.set_font('Arial', 'B', 9)
        pdf.set_x(pdf.l_margin)
        pdf.cell(0, 4, clean(f'{comp.name}:'), border=0,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('Arial', '', 9)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(_safe_width(pdf), 4,
                       clean(f'  Differentiation: {comp.differentiation_notes}'))
        if comp.exploitable_gap:
            pdf.set_font('Arial', 'I', 9)
            pdf.set_text_color(31, 119, 180)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(_safe_width(pdf), 4,
                           clean(f'  Exploitable Gap: {comp.exploitable_gap}'))
            pdf.set_text_color(0, 0, 0)
        pdf.ln(1.5)

    pdf.ln(2)
    pdf.section_title('Differentiation Hints')
    for hint in blueprint.market_research.differentiation_hints:
        pdf.bullet_point(hint)

    # Section 2: ICP & Personas
    pdf.add_page()
    pdf.chapter_title('2. ICP & Buyer Personas')

    pdf.section_title('Ideal Customer Profile')
    icp = blueprint.icp_and_personas.icp
    pdf.label('Company Size:')
    pdf.small_text(icp.company_size, indent=5)
    pdf.label('Budget Level:')
    pdf.small_text(icp.budget_level, indent=5)
    pdf.label('Industries:')
    for ind in icp.industries:
        pdf.small_text(f'- {ind}', indent=5)
    pdf.label('Geography:')
    for geo in icp.geography:
        pdf.small_text(f'- {geo}', indent=5)
    pdf.label('Tech Stack:')
    for tech in icp.tech_stack:
        pdf.small_text(f'- {tech}', indent=5)
    pdf.ln(3)
    pdf.horizontal_line()

    for idx, persona in enumerate(blueprint.icp_and_personas.personas, 1):
        if pdf.get_y() > 220:
            pdf.add_page()
        pdf.subsection_title(f'Persona {idx}: {persona.name} - {persona.role}')

        if persona.company_stage:
            pdf.set_font('Arial', 'I', 9)
            pdf.set_text_color(80, 80, 80)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(_safe_width(pdf), 4,
                           clean(f'Company Stage: {persona.company_stage}'))
            pdf.set_text_color(0, 0, 0)
            pdf.ln(1)
        if persona.day_in_the_life:
            pdf.info_box(persona.day_in_the_life, bg_color=(245, 245, 245))

        pdf.label('Responsibilities:')
        pdf.small_text(persona.responsibilities, indent=3)
        pdf.ln(1)

        if persona.current_tools:
            pdf.label('Current Tools:')
            for tool in persona.current_tools:
                pdf.small_text(f'- {tool}', indent=3)
            pdf.ln(1)

        pdf.label('Pains:')
        for pain in persona.pains:
            pdf.small_text(f'- {pain}', indent=3)
        pdf.ln(1)

        pdf.label('Goals:')
        for goal in persona.goals:
            pdf.small_text(f'- {goal}', indent=3)
        pdf.ln(1)

        pdf.label('Buying Triggers:')
        for trigger in persona.buying_triggers:
            pdf.small_text(f'- {trigger}', indent=3)
        pdf.ln(1)

        pdf.label('Objections:')
        for obj in persona.objections:
            pdf.small_text(f'- {obj}', indent=3)
        pdf.ln(1)

        pdf.label('Success Criteria:')
        pdf.info_box(persona.success_criteria, bg_color=(240, 255, 240))

        if idx < len(blueprint.icp_and_personas.personas):
            pdf.ln(2)
            pdf.horizontal_line()

    # Section 3: Positioning
    pdf.add_page()
    pdf.chapter_title('3. Positioning & Messaging')

    pdf.section_title('Positioning Statement')
    pdf.info_box(blueprint.positioning.positioning_statement)
    pdf.ln(2)

    pdf.section_title('Value Propositions')
    for i, vp in enumerate(blueprint.positioning.value_propositions, 1):
        pdf.bullet_point(vp, symbol=f'{i}.')
        pdf.ln(0.5)

    pdf.ln(3)
    pdf.section_title('Persona-Specific Messages')
    for pm in blueprint.positioning.persona_messages:
        pdf.subsection_title(pm.persona_name)
        pdf.italic_text(f'"{pm.headline}"')
        for bullet in pm.key_bullets:
            pdf.small_text(f'- {bullet}', indent=3)
        pdf.ln(2)

    # Section 4: Channel Plan
    pdf.add_page()
    pdf.chapter_title('4. Channel & Experiment Strategy')

    pdf.section_title('Primary Channels')
    for ch in blueprint.channel_plan.primary_channels:
        pdf.subsection_title(f'{ch.name}  (Effort: {ch.effort})')
        if ch.target_persona:
            pdf.set_font('Arial', 'I', 9)
            pdf.set_text_color(31, 119, 180)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(_safe_width(pdf), 4,
                           clean(f'Reaches: {ch.target_persona}'))
            pdf.set_text_color(0, 0, 0)
        pdf.small_text(ch.rationale, indent=3)
        if ch.monthly_reach:
            pdf.small_text(f'Est. monthly reach: {ch.monthly_reach}', indent=3)
        if ch.first_action:
            pdf.set_font('Arial', 'B', 9)
            pdf.set_text_color(46, 139, 87)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(_safe_width(pdf), 4,
                           clean(f'First action: {ch.first_action}'))
            pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

    pdf.ln(2)
    pdf.section_title('Prioritized Experiments')
    exp_headers = ['#', 'Experiment', 'Goal', 'Effort',
                   'Timing', 'ICE', 'Baseline -> Target']
    exp_rows = [
        [
            str(i),
            exp.name,
            exp.goal,
            exp.effort,
            exp.timing,
            str(exp.ice_score) if exp.ice_score is not None else '-',
            f'{exp.baseline or "-"}  ->  {exp.target or "-"}',
        ]
        for i, exp in enumerate(blueprint.channel_plan.experiments, 1)
    ]
    pdf.render_table_multiline(exp_headers, exp_rows,
                               col_widths=[8, 32, 38, 15, 22, 12, 53])

    pdf.section_title('Experiment Details')
    for i, exp in enumerate(blueprint.channel_plan.experiments, 1):
        pdf.label(f'{i}. {exp.name}')
        if exp.ice_score is not None:
            pdf.ice_badge(exp.ice_score)
        if exp.depends_on:
            pdf.set_font('Arial', 'I', 8)
            pdf.set_text_color(100, 100, 100)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(_safe_width(pdf), 4,
                           clean(f'Builds on: {exp.depends_on}'))
            pdf.set_text_color(0, 0, 0)
        pdf.small_text(f'Goal: {exp.goal}', indent=3)
        if exp.description:
            pdf.small_text(f'Description: {exp.description}', indent=3)
        if exp.baseline and exp.target:
            pdf.set_font('Arial', 'B', 9)
            pdf.set_text_color(44, 62, 80)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(_safe_width(pdf), 4,
                           clean(f'  Baseline: {exp.baseline}  ->  Target: {exp.target}'))
            pdf.set_text_color(0, 0, 0)
        pdf.small_text(f'Success Metric: {exp.success_metric}', indent=3)
        pdf.ln(2)

    # Section 5: Metrics & Risks
    pdf.add_page()
    pdf.chapter_title('5. Metrics & Risks')

    if blueprint.metrics_and_risks.north_star_metric:
        pdf.section_title('North Star Metric')
        pdf.north_star_badge(blueprint.metrics_and_risks.north_star_metric)

    pdf.section_title('Primary KPIs')
    for kpi in blueprint.metrics_and_risks.primary_kpis:
        pdf.kpi_row(kpi, is_north_star=kpi.is_north_star)
    pdf.ln(3)

    pdf.section_title('GTM Funnel')
    for stage in blueprint.metrics_and_risks.funnel:
        pdf.subsection_title(f'{stage.stage}')
        pdf.small_text(stage.description, indent=3)
        if stage.conversion_rate:
            pdf.set_font('Arial', 'B', 9)
            pdf.set_text_color(31, 119, 180)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(_safe_width(pdf), 4,
                           clean(f'   Conversion: {stage.conversion_rate}'))
            pdf.set_text_color(0, 0, 0)
        pdf.italic_text(f'   Example: {stage.example_metric}')
        pdf.ln(1)

    pdf.ln(2)
    pdf.section_title('Risk Assessment Table')
    risk_headers = ['Risk', 'Impact', 'Likelihood', 'Mitigation', 'Owner']
    risk_rows = [
        [
            risk.risk,
            risk.impact,
            risk.likelihood,
            risk.mitigation,
            risk.owner or '-',
        ]
        for risk in blueprint.metrics_and_risks.risks
    ]
    pdf.render_table_multiline(risk_headers, risk_rows,
                               col_widths=[50, 18, 22, 65, 25])

    pdf.section_title('Risk Details')
    for risk in blueprint.metrics_and_risks.risks:
        pdf.set_font('Arial', 'B', 9)
        pdf.set_x(pdf.l_margin)
        pdf.cell(0, 4, clean(risk.risk), border=0,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.risk_badge(risk.impact)
        pdf.set_font('Arial', '', 8)
        pdf.cell(20, 5, 'Impact', border=0,
                 new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.risk_badge(risk.likelihood)
        pdf.set_font('Arial', '', 8)
        pdf.cell(0, 5, 'Likelihood', border=0,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('Arial', '', 9)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(_safe_width(pdf), 4,
                       clean(f'Mitigation: {risk.mitigation}'))
        if risk.early_warning_signal:
            pdf.set_font('Arial', 'I', 8)
            pdf.set_text_color(180, 0, 0)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(_safe_width(pdf), 4,
                           clean(f'Early Warning: {risk.early_warning_signal}'))
            pdf.set_text_color(0, 0, 0)
        if risk.owner:
            pdf.set_font('Arial', 'I', 8)
            pdf.set_text_color(80, 80, 80)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(_safe_width(pdf), 4,
                           clean(f'Owner: {risk.owner}'))
            pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

    # Section 6: Action Plan
    pdf.add_page()
    pdf.chapter_title(
        f'6. {blueprint.action_plan.timeline_weeks}-Week GTM Action Plan')

    weekly = blueprint.action_plan.weekly_actions
    for i, wa in enumerate(weekly):
        pdf.subsection_title(f'Week {wa.week} -- {wa.focus}')
        for action in wa.actions:
            pdf.bullet_point(action)
        pdf.ln(2)
        if i < len(weekly) - 1:
            pdf.set_draw_color(230, 230, 230)
            pdf.line(pdf.l_margin, pdf.get_y(),
                     pdf.w - pdf.r_margin, pdf.get_y())
            pdf.ln(2)

    # Section 7: Next Steps
    pdf.add_page()
    pdf.chapter_title('7. Next Steps -- Founder Checklist')
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(_safe_width(pdf), 5,
                   'Complete these 7 actions in the next 7 days to launch your GTM:')
    pdf.ln(3)

    for i, step in enumerate(blueprint.next_steps, 1):
        pdf.checkbox_item(f'{i}. {step}')
        pdf.ln(0.5)

    buffer = BytesIO()
    buffer.write(pdf.output())
    buffer.seek(0)
    return buffer
