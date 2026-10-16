# Wealth Advisor Assistant — Mini Multi-Agent System

A small, modular Python demonstration for the AI Engineer (Agent Systems) assignment. It ingests client JSON, calls mock CRM/market tools through abstractions, calculates financial metrics, flags unusual expenses, writes a structured JSON report, logs execution, and offers an optional human-review checkpoint.

## Features mapped to the assignment

- **Orchestrator Agent:** coordinates the workflow and error/fallback behavior.
- **Data Fetcher Agent:** validates input and retrieves mock CRM and market context.
- **Analyzer Agent:** calculates income, expenses, net cash flow, savings rate, category totals, and rule-based anomaly flags.
- **Tool abstraction:** agents call interfaces in `tools/`, not raw API implementations.
- **Error handling:** invalid input produces a structured error; malformed transactions are skipped with warnings.
- **Logging:** execution details and errors are written to `agent_system.log`.
- **Memory layer:** current-run state acts as short-term memory; compact historical summaries are stored in `data/memory_summaries.json`.
- **Human-in-the-loop:** the default run asks an operator to approve or reject the generated demo report.

## Requirements

- Python 3.10 or later
- No third-party dependencies

## Run locally

1. Unzip the project.
2. Open a terminal in the project directory.
3. Run:

   ```bash
   python main.py
   ```

4. At the review prompt, enter `y` to approve or press Enter to leave it unapproved.
5. The report is saved to `output/advisory_report.json`; logs are saved to `agent_system.log`.

For a non-interactive run:

```bash
python main.py --no-approval
```

To use a different input file:

```bash
python main.py --input data/client_financial_data.json --no-approval
```

## Architecture and flow

```text
JSON input
   |
   v
OrchestratorAgent
   |
   +--> DataFetcherAgent --> MockCRMTool
   |                    +--> MockMarketContextTool
   |
   +--> AnalyzerAgent --> financial metrics + anomaly rules
   |
   +--> ReportTool --> structured report
   |
   +--> Human review checkpoint
   |
   +--> MemoryTool --> historical summary JSON
```

## Sample output shape

```json
{
  "status": "success",
  "client": {
    "client_id": "CL-1001",
    "name": "Sample Client",
    "currency": "INR"
  },
  "analysis": {
    "income_total": 65000.0,
    "expense_total": 87200.0,
    "net_cash_flow": -22200.0,
    "savings_rate_percent": -34.15,
    "anomalies": []
  },
  "human_review": {
    "required": true,
    "status": "pending"
  }
}
```

Actual values and anomaly flags are calculated at runtime and may differ from this illustrative shape.

## Anomaly detection approach

This demo flags expenses above `max(3 * median_expense, 5000)`. This transparent rule is easy to explain and tune. It is **not** a trained model and does not establish fraud. In production, thresholds should be validated against historical data, transaction categories, client-specific behavior, false-positive costs, and human review.

## Assumptions and trade-offs

1. CRM and market context are mocked because API credentials and provider details were not supplied.
2. A deterministic, rule-based analyzer keeps the project runnable without an LLM key or paid service.
3. Financial amounts use the input currency (INR in the sample); no currency conversion is performed.
4. Missing/invalid individual transactions are skipped with warnings; missing required top-level fields stop the workflow.
5. The memory layer stores compact summaries only. Avoid storing real personal or financial data without appropriate consent, access controls, encryption, and retention policies.
6. The human checkpoint is a simple terminal prompt rather than a full approval UI.
7. This tool produces educational insights, not regulated personalized financial advice.

## Extending the project

- Replace mock tool methods with authenticated HTTP clients and timeout/retry policies.
- Add unit tests and schema validation.
- Use a database for persistent memory with access controls and retention policies.
- Add an LLM only if needed for natural-language explanations, with strict structured-output validation and no autonomous transactions.
- Add a dashboard or API layer after the CLI workflow is stable.

## Repository submission checklist

- [ ] Run `python main.py` successfully.
- [ ] Inspect `output/advisory_report.json`.
- [ ] Confirm `agent_system.log` is created.
- [ ] Confirm `data/memory_summaries.json` is created.
- [ ] Add screenshots of the successful run to the repository if requested.
- [ ] Upload the source to GitHub and include this README.
