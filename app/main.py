import os
import time
import math
from datetime import datetime
import plotext as plt
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from rich.live import Live

from analyzer import RevenueAnalyzer
from ai_engine import InsightEngine

console = Console()

# Bloomberg color palette
TERM_COLOR = "orange1"
TERM_BORDER = "cyan"
TERM_BG = "black"

def create_header():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header_text = f" ▉ HEPHAESTUS FINANCIAL TERMINAL ▉   SYSTEM: LIVE   |   DATETIME: {now}   |   USER: ADMIN "
    return Panel(
        Text(header_text, style=f"bold {TERM_BORDER} on {TERM_BG}", justify="center"),
        style=f"on {TERM_BG}",
        border_style=TERM_BORDER
    )

def setup_plotext_theme():
    # Use a pre-defined theme for black background
    plt.theme('dark')
    # Use standard plotext methods for colors if needed, but 'dark' works

def create_funnel_ansi(metrics):
    plt.clf()
    setup_plotext_theme()
    # Dynamic sizing based on terminal width/height can be tricky inside layout,
    # so we use a reasonable fixed/constrained size
    plt.plotsize(plt.tw() // 2 if plt.tw() else 50, 12)
    plt.title("CUSTOMER JOURNEY FUNNEL")
    
    stages = []
    users = []
    
    for row in reversed(metrics['funnel']):
        stages.append(row['event_type'].replace('_', ' ').title())
        users.append(int(row['users']))
        
    plt.bar(stages, users, orientation="horizontal", color="yellow")
    return plt.build()

def create_roi_ansi(metrics):
    plt.clf()
    setup_plotext_theme()
    plt.plotsize(plt.tw() // 2 if plt.tw() else 40, 15)
    plt.title("MARKETING ROI (%)")
    
    sources = []
    rois = []
    colors = []
    
    for row in metrics.get('roi', []):
        sources.append(row['source'])
        roi_val = row['roi_percent']
        if math.isinf(roi_val):
            roi_val = 1500 # Cap for plot
        rois.append(roi_val)
        colors.append("yellow" if roi_val > 0 else "red")
        
    plt.bar(sources, rois, color=colors)
    return plt.build()

def render_financial_impact(metrics):
    top_leak = metrics['top_leak_stage'].replace('_', ' ').title()
    leak_value = f"${metrics['top_leak_value']:,.2f}"
    
    impact_text = Text(style=f"{TERM_COLOR} on {TERM_BG}")
    impact_text.append("[!]", style="bold red blink")
    impact_text.append(" CRITICAL LEAK IDENTIFIED: ", style="bold red")
    impact_text.append(top_leak, style="bold underline red")
    impact_text.append("\n\n")
    impact_text.append("  > Estimated Monthly Recovery Potential: ", style=f"bold {TERM_COLOR}")
    impact_text.append(leak_value, style=f"bold {TERM_COLOR} reverse")
    
    return Panel(
        Align.center(impact_text, vertical="middle"), 
        border_style="red", 
        title="[bold red]SYSTEM ALERT[/bold red]", 
        padding=(1, 2)
    )

def render_funnel(metrics):
    ansi_plot = create_funnel_ansi(metrics)
    return Panel(
        Align.center(Text.from_ansi(ansi_plot)),
        title=f"[bold {TERM_BORDER}]FUNNEL METRICS[/bold {TERM_BORDER}]",
        border_style=TERM_BORDER,
        style=f"on {TERM_BG}"
    )

def render_marketing_roi(metrics):
    ansi_plot = create_roi_ansi(metrics)
    return Panel(
        Align.center(Text.from_ansi(ansi_plot)),
        title=f"[bold {TERM_BORDER}]MARKETING P&L[/bold {TERM_BORDER}]",
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

def make_layout() -> Layout:
    layout = Layout(name="root")
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
    )
    layout["main"].split_row(
        Layout(name="left", ratio=6),
        Layout(name="right", ratio=4)
    )
    layout["left"].split_column(
        Layout(name="impact", size=8),
        Layout(name="funnel")
    )
    layout["right"].split_column(
        Layout(name="roi", ratio=1),
        Layout(name="ai_insights", ratio=1)
    )
    return layout

def main():
    console.clear()
    
    # 1. Loading Phase
    with Progress(
        SpinnerColumn(style=TERM_BORDER),
        TextColumn(f"[{TERM_COLOR}][progress.description]{{task.description}}[/{TERM_COLOR}]"),
        transient=True,
    ) as progress:
        task1 = progress.add_task(description="Fetching market behaviors...", total=None)
        time.sleep(1.0)
        analyzer = RevenueAnalyzer()
        metrics = analyzer.get_summary_metrics()
        progress.update(task1, description="Fetching market behaviors... DONE")
        
        task2 = progress.add_task(description="Calculating financial upside...", total=None)
        time.sleep(0.5)
        progress.update(task2, description="Calculating financial upside... DONE")
        
        task3 = progress.add_task(description="Querying AI Oracle (Gemini)...", total=None)
        engine = InsightEngine()
        insights = engine.generate_insights(metrics)
        progress.update(task3, description="Querying AI Oracle... DONE")

    # 2. Build Layout
    layout = make_layout()
    layout["header"].update(create_header())
    layout["impact"].update(render_financial_impact(metrics))
    layout["funnel"].update(render_funnel(metrics))
    layout["roi"].update(render_marketing_roi(metrics))
    layout["ai_insights"].update(render_ai_insights(insights))
    
    # 3. Print the layout once (Bloomberg terminal view)
    console.print(layout)
    
if __name__ == "__main__":
    main()

