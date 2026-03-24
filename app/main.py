import os
import time
import math
import plotext as plt
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from rich.style import Style

from analyzer import RevenueAnalyzer
from ai_engine import InsightEngine

console = Console()

def print_header():
    console.clear()
    header = Text(" ▉ REVENUE LEAK DETECTOR ████ FINANCIAL TERMINAL ▉ ", style="bold green on black", justify="center")
    console.print(Panel(header, border_style="green", padding=(1, 1)), justify="center")
    console.print("\n")

def create_funnel_ansi(metrics):
    plt.clf()
    # Matrix theme matches the wall street terminal vibe
    plt.theme("matrix")
    plt.plotsize(70, 15)
    plt.title("CUSTOMER JOURNEY FUNNEL")
    
    stages = []
    users = []
    
    # We want top to bottom funnel, so reverse the order for plotext
    for row in reversed(metrics['funnel']):
        stages.append(row['event_type'].replace('_', ' ').title())
        users.append(int(row['users']))
        
    plt.bar(stages, users, orientation="horizontal", color="green")
    return plt.build()

def display_funnel(metrics):
    ansi_plot = create_funnel_ansi(metrics)
    panel = Panel(
        Text.from_ansi(ansi_plot),
        title="[bold green]FUNNEL METRICS[/bold green]",
        border_style="green",
        expand=False
    )
    console.print(Align.center(panel))
    console.print("\n")

def create_roi_ansi(metrics):
    plt.clf()
    plt.theme("matrix")
    plt.plotsize(70, 15)
    plt.title("MARKETING ROI (%)")
    
    sources = []
    rois = []
    colors = []
    
    for row in metrics.get('roi', []):
        sources.append(row['source'])
        roi_val = row['roi_percent']
        if math.isinf(roi_val):
            roi_val = 1000 # Cap it for plotting
        rois.append(roi_val)
        colors.append("green" if roi_val > 0 else "red")
        
    plt.bar(sources, rois, color=colors)
    return plt.build()

def display_marketing_roi(metrics):
    ansi_plot = create_roi_ansi(metrics)
    panel = Panel(
        Text.from_ansi(ansi_plot),
        title="[bold green]MARKETING PERFORMANCE[/bold green]",
        border_style="green",
        expand=False
    )
    console.print(Align.center(panel))
    console.print("\n")

def display_financial_impact(metrics):
    top_leak = metrics['top_leak_stage'].replace('_', ' ').title()
    leak_value = f"${metrics['top_leak_value']:,.2f}"
    
    impact_text = Text()
    impact_text.append("[!]", style="bold red blink")
    impact_text.append(" CRITICAL LEAK IDENTIFIED: ", style="bold red")
    impact_text.append(top_leak, style="bold underline red")
    impact_text.append("\n\n")
    impact_text.append("  > Estimated Monthly Recovery Potential: ", style="bold green")
    impact_text.append(leak_value, style="bold green reverse")
    
    panel = Panel(impact_text, border_style="red", title="[bold red]SYSTEM ALERTMESSAGE[/bold red]", expand=False, padding=(1,4))
    console.print(Align.center(panel))
    console.print("\n")

def display_ai_insights(insights):
    panel = Panel(
        insights,
        title="[bold green]AI DIAGNOSTICS & RECOMMENDATIONS[/bold green]",
        border_style="green",
        padding=(1, 3),
        expand=False
    )
    console.print(Align.center(panel))
    console.print("\n")

def main():
    print_header()
    
    with Progress(
        SpinnerColumn(style="green"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task1 = progress.add_task(description="[green]Fetching market demographic behaviors...[/green]", total=None)
        time.sleep(1.0)
        analyzer = RevenueAnalyzer()
        metrics = analyzer.get_summary_metrics()
        progress.update(task1, description="[green]Fetching market demographic behaviors... DONE[/green]")
        
        task2 = progress.add_task(description="[green]Calculating financial upside...[/green]", total=None)
        time.sleep(0.5)
        progress.update(task2, description="[green]Calculating financial upside... DONE[/green]")
        
        task3 = progress.add_task(description="[green]Connecting to prediction engine...[/green]", total=None)
        engine = InsightEngine()
        insights = engine.generate_insights(metrics)
        progress.update(task3, description="[green]Connecting to prediction engine... DONE[/green]")

    display_financial_impact(metrics)
    display_funnel(metrics)
    display_marketing_roi(metrics)
    display_ai_insights(insights)
    
if __name__ == "__main__":
    main()

