import os
import time
import math
from datetime import datetime
import plotext as plt
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn

from analyzer import RevenueAnalyzer
from ai_engine import InsightEngine

console = Console()

# Bloomberg color palette
TERM_COLOR = "orange1"
TERM_BORDER = "cyan"
TERM_BG = "black"

def setup_plotext_theme():
    plt.theme('dark')

def create_header(metrics):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    val_col = metrics.get('value_col', 'N/A')
    total = metrics.get('total_value', 0)
    rows = metrics.get('total_rows', 0)
    margin = metrics.get('margin_pct', None)
    
    parts = [f" ▉ HEPHAESTUS ▉  {now}  |  {val_col}: ${total:,.0f}  |  ROWS: {rows}"]
    if margin is not None:
        parts.append(f"  |  MARGIN: {margin}%")
    parts.append("  |  LIVE ")
    
    return Panel(
        Text("".join(parts), style=f"bold {TERM_BORDER} on {TERM_BG}", justify="center"),
        style=f"on {TERM_BG}",
        border_style=TERM_BORDER
    )

def render_kpi_bar(metrics):
    kpi = Text(style=f"{TERM_COLOR} on {TERM_BG}")
    
    leak = metrics.get('total_leak_value', 0)
    worst = metrics.get('worst_category', 'N/A')
    
    kpi.append("[!]", style="bold red blink")
    kpi.append(f" LEAKS: ", style="bold red")
    kpi.append(f"${leak:,.0f}", style="bold red reverse")
    kpi.append("  |  ", style="dim")
    
    if 'total_loss' in metrics:
        kpi.append(f"EROSION: ", style=f"bold {TERM_COLOR}")
        kpi.append(f"${metrics['total_loss']:,.0f}", style=f"bold {TERM_COLOR}")
        kpi.append("  |  ", style="dim")
    
    kpi.append(f"WEAKEST: ", style=f"bold {TERM_COLOR}")
    kpi.append(worst, style=f"bold {TERM_COLOR} underline")
    
    return Panel(
        Align.center(kpi, vertical="middle"),
        border_style="red",
        title="[bold red]SYSTEM ALERT[/bold red]",
        style=f"on {TERM_BG}"
    )

def create_bar_chart(labels, values, title, width, height=10, horizontal=False):
    """Create a responsive bar chart that fits within the given width."""
    plt.clf()
    setup_plotext_theme()
    # Constrain plot size to available panel width (subtract borders/padding)
    plot_w = max(15, width - 4)
    plt.plotsize(plot_w, height)
    plt.title(title)
    
    # Truncate long labels for readability
    max_label_len = 12 if not horizontal else 15
    short_labels = [str(l)[:max_label_len] for l in labels]
    
    colors = ["yellow" if v >= 0 else "red" for v in values]
    
    if horizontal:
        plt.bar(short_labels, values, orientation="horizontal", color=colors)
    else:
        plt.bar(short_labels, values, color=colors)
    
    return plt.build()

def render_chart_panel(ansi_plot, title):
    return Panel(
        Text.from_ansi(ansi_plot),
        title=f"[bold {TERM_BORDER}]{title}[/bold {TERM_BORDER}]",
        border_style=TERM_BORDER,
        style=f"on {TERM_BG}"
    )

def render_ai_insights(insights):
    return Panel(
        Text(insights, style=f"{TERM_COLOR}"),
        title=f"[bold {TERM_BORDER}]AI DIRECTIVES[/bold {TERM_BORDER}]",
        border_style=TERM_BORDER,
        padding=(1, 2),
        style=f"on {TERM_BG}"
    )

def build_charts(metrics, half_w):
    """Auto-generate chart panels from whatever groups were detected."""
    charts = []
    groups = metrics.get('groups', {})
    value_col = metrics.get('value_col', 'value')
    sum_key = f'{value_col}_sum'
    
    for group_name, records in groups.items():
        if not records:
            continue
        labels = [r[group_name] for r in records]
        values = [r.get(sum_key, 0) for r in records]
        
        title = f"{value_col.upper()} BY {group_name.upper()}"
        
        # Use horizontal bars if many categories
        horizontal = len(labels) > 5
        chart_height = max(8, min(12, len(labels) + 4))
        
        ansi = create_bar_chart(labels, values, title, half_w, height=chart_height, horizontal=horizontal)
        charts.append(render_chart_panel(ansi, title))
    
    return charts

def make_layout(num_charts) -> Layout:
    layout = Layout(name="root")
    
    if num_charts >= 2:
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="alert", size=5),
            Layout(name="charts_row"),
            Layout(name="bottom")
        )
        layout["charts_row"].split_row(
            Layout(name="chart_0"),
            Layout(name="chart_1")
        )
        layout["bottom"].split_row(
            Layout(name="chart_2") if num_charts >= 3 else Layout(name="ai_only_left"),
            Layout(name="ai_insights")
        )
    elif num_charts == 1:
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="alert", size=5),
            Layout(name="charts_row"),
            Layout(name="bottom")
        )
        layout["charts_row"].update(Layout(name="chart_0"))
        layout["bottom"].update(Layout(name="ai_insights"))
    else:
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="alert", size=5),
            Layout(name="ai_insights")
        )
    
    return layout

def main():
    console.clear()
    
    with Progress(
        SpinnerColumn(style=TERM_BORDER),
        TextColumn(f"[{TERM_COLOR}][progress.description]{{task.description}}[/{TERM_COLOR}]"),
        transient=True,
    ) as progress:
        task1 = progress.add_task(description="Loading data...", total=None)
        time.sleep(0.3)
        analyzer = RevenueAnalyzer()
        metrics = analyzer.get_summary_metrics()
        progress.update(task1, description="Loading data... DONE")
        
        task2 = progress.add_task(description="Querying AI Oracle...", total=None)
        engine = InsightEngine()
        insights = engine.generate_insights(metrics)
        progress.update(task2, description="Querying AI Oracle... DONE")

    term_w, term_h = console.size
    half_w = max(20, term_w // 2 - 2)
    
    chart_panels = build_charts(metrics, half_w)
    num_charts = len(chart_panels)
    
    layout = make_layout(num_charts)
    layout["header"].update(create_header(metrics))
    layout["alert"].update(render_kpi_bar(metrics))
    
    # Assign charts
    for i, panel in enumerate(chart_panels[:3]):
        key = f"chart_{i}"
        try:
            layout[key].update(panel)
        except KeyError:
            break
    
    # If we have < 3 charts and chart_2 slot exists, fill it
    if num_charts < 3:
        try:
            layout["ai_only_left"].update(Panel(
                Text("No additional data dimensions detected.", style=f"dim {TERM_COLOR}"),
                border_style=TERM_BORDER,
                style=f"on {TERM_BG}"
            ))
        except KeyError:
            pass
    
    layout["ai_insights"].update(render_ai_insights(insights))
    
    console.print(layout)

if __name__ == "__main__":
    main()
