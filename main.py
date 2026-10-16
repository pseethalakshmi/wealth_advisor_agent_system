from agents.orchestrator import OrchestratorAgent
from tools.crm_tool import MockCRMTool
from tools.market_tool import MockMarketContextTool
from tools.memory_tool import MemoryTool
from tools.report_tool import ReportTool
import argparse
import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("agent_system.log", encoding="utf-8")],
)

def main():
    parser = argparse.ArgumentParser(description="Mini multi-agent Wealth Advisor Assistant")
    parser.add_argument("--input", default="data/client_financial_data.json", help="Path to client JSON input")
    parser.add_argument("--no-approval", action="store_true", help="Skip the optional human review checkpoint")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    try:
        client_data = json.loads(input_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise SystemExit(f"Could not read valid JSON input: {exc}")

    tools = {
        "crm": MockCRMTool(),
        "market": MockMarketContextTool(),
        "memory": MemoryTool(),
        "report": ReportTool(),
    }
    orchestrator = OrchestratorAgent(tools)
    result = orchestrator.run(client_data, require_approval=not args.no_approval)

    output_path = Path("output/advisory_report.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"\nReport saved to: {output_path}")
    print("Execution log saved to: agent_system.log")

if __name__ == "__main__":
    main()
