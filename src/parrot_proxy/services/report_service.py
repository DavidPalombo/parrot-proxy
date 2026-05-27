from pathlib import Path

from parrot_proxy.core.reporting_engine import generate_markdown_report

def write_markdown_report(campaign_name: str, workflow_results: list,):
    report = generate_markdown_report(
        campaign_name = campaign_name,
        workflow_results = workflow_results,
    )

    reports_dir = Path("reports")

    reports_dir.mkdir(exist_ok = True)

    output_path = (
        reports_dir /
        f"{campaign_name}.md"
    )
    
    output_path.write_text(report)

    return output_path