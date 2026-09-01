# AI Research & Report Agent

A production-oriented multi-agent AI research system built with the **OpenAI Agents SDK**, supporting both **OpenAI** and **Groq**.

The system uses two specialized agents:

```text
User
  │
  ▼
┌─────────────────────────┐
│     Research Agent      │
│                         │
│ • Identifies trends     │
│ • Performs web research │
│ • Collects evidence    │
│ • Estimates investment  │
│ • Calculates metrics    │
└────────────┬────────────┘
             │
             │ Handoff
             ▼
┌─────────────────────────┐
│   Report Writer Agent   │
│                         │
│ • Organizes research   │
│ • Validates findings   │
│ • Calculates summary   │
│ • Produces Markdown     │
└────────────┬────────────┘
             │
             ▼
       Final Report
```

The default research task is:

> Research the top 5 emerging AI trends in 2024, analyze their potential market impact, calculate average investment needed, and generate a structured report.

---

# Features

* OpenAI Agents SDK
* OpenAI API support
* Groq API support
* Multi-agent architecture
* Native agent handoff
* Research Agent
* Report Writer Agent
* Web search tool
* Tavily integration
* Deterministic search simulator for development
* Data analysis/calculation tool
* Optional Markdown file-writing tool
* Exponential backoff
* API rate-limit handling
* Timeout handling
* Network error handling
* Structured logging
* Environment-variable configuration
* FastAPI REST API
* Swagger/OpenAPI documentation
* Windows 11 / PowerShell support
* Automated tests with pytest
* Render deployment configuration
* GitHub-ready repository

---

# Project Structure

```text
ai-research-agent/
│
├── agent.py
├── tools.py
├── api.py
├── test_agent.py
│
├── requirements.txt
├── .env.example
├── .gitignore
├── render.yaml
├── README.md
│
└── reports/
```

## File Responsibilities

### `agent.py`

Main AI orchestration layer.

Contains:

* Research Agent
* Report Writer Agent
* OpenAI/Groq model configuration
* Agent handoff
* Agent execution
* Retry handling
* CLI entry point

### `tools.py`

Contains all custom agent tools:

```text
web_search()
calculate_statistics()
save_report()
```

### `api.py`

FastAPI HTTP interface.

Endpoints:

```text
GET  /health
POST /research
```

### `test_agent.py`

Unit tests for the calculation tool and project configuration.

### `requirements.txt`

Python dependencies.

### `.env.example`

Environment-variable template.

### `render.yaml`

Render deployment configuration.

### `.gitignore`

Prevents secrets and local Python files from being committed.

---

# Architecture

The project uses a two-agent architecture.

## Agent 1 — Research Agent

The Research Agent is responsible for gathering and analyzing information.

It can use:

```text
web_search
calculate_statistics
```

Its workflow is:

```text
User Request
     │
     ▼
Research Agent
     │
     ├── Search overall AI trends
     │
     ├── Search Trend #1
     │
     ├── Search Trend #2
     │
     ├── Search Trend #3
     │
     ├── Search Trend #4
     │
     ├── Search Trend #5
     │
     ├── Research market impact
     │
     ├── Research investment requirements
     │
     └── Calculate average investment
             │
             ▼
       Research Complete
             │
             ▼
          Handoff
             │
             ▼
       Report Writer Agent
```

## Agent 2 — Report Writer Agent

The Report Writer Agent receives the research context through the agent handoff.

It is responsible for producing the final structured report.

It can use:

```text
calculate_statistics
save_report
```

The final report contains:

1. Executive Summary
2. Top 5 AI Trends
3. Supporting Evidence
4. Market Impact
5. Investment Requirements
6. Average Investment
7. Risks and Assumptions
8. Conclusion
9. Sources

---

# Agent Handoff

The project uses the Agents SDK's native handoff mechanism.

Conceptually:

```python
research_agent = Agent(
    name="Research Agent",
    tools=[
        web_search,
        calculate_statistics,
    ],
    handoffs=[
        handoff(report_writer_agent)
    ],
)
```

The Research Agent remains responsible for research.

Once its research is complete, it hands control to:

```text
Report Writer Agent
```

The Report Writer then produces the final answer.

This separation keeps research and report generation independent.

---

# Requirements

## Software

Recommended:

```text
Windows 11
Python 3.11+
PowerShell 5.1+ or PowerShell 7+
Git
```

## API Keys

You need at least one:

```text
OpenAI API Key
```

or:

```text
Groq API Key
```

For real web search, also configure:

```text
Tavily API Key
```

---

# Windows 11 Setup

Open PowerShell.

Create the project directory:

```powershell
New-Item -ItemType Directory -Path "ai-research-agent" -Force
```

Enter the directory:

```powershell
Set-Location "ai-research-agent"
```

---

# Create Python Virtual Environment

Check Python:

```powershell
python --version
```

or:

```powershell
py --version
```

Recommended Python version:

```text
Python 3.11+
```

Create the virtual environment:

```powershell
py -3.11 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Your PowerShell prompt should now show something similar to:

```text
(.venv) PS C:\...\ai-research-agent>
```

---

# PowerShell Execution Policy

If you receive:

```text
running scripts is disabled on this system
```

run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

# Upgrade pip

```powershell
python -m pip install --upgrade pip
```

---

# Install Dependencies

Run:

```powershell
pip install -r requirements.txt
```

Verify:

```powershell
pip list
```

---

# Environment Configuration

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Open it:

```powershell
notepad .env
```

---

# OpenAI Configuration

To use OpenAI:

```env
LLM_PROVIDER=openai

OPENAI_API_KEY=YOUR_OPENAI_API_KEY

OPENAI_MODEL=gpt-4o-mini

GROQ_API_KEY=

GROQ_MODEL=llama-3.3-70b-versatile

TAVILY_API_KEY=

LOG_LEVEL=INFO

MAX_RETRIES=4

REQUEST_TIMEOUT_SECONDS=30

PORT=8000
```

Replace:

```text
YOUR_OPENAI_API_KEY
```

with your actual OpenAI API key.

---

# Groq Configuration

To use Groq instead:

```env
LLM_PROVIDER=groq

OPENAI_API_KEY=

OPENAI_MODEL=gpt-4o-mini

GROQ_API_KEY=YOUR_GROQ_API_KEY

GROQ_MODEL=llama-3.3-70b-versatile

TAVILY_API_KEY=

LOG_LEVEL=INFO

MAX_RETRIES=4

REQUEST_TIMEOUT_SECONDS=30

PORT=8000
```

Replace:

```text
YOUR_GROQ_API_KEY
```

with your actual key.

Groq exposes an OpenAI-compatible API, allowing the project to use the same overall model abstraction.

---

# Tavily Web Search

The project supports Tavily for real web research.

Set:

```env
TAVILY_API_KEY=YOUR_TAVILY_API_KEY
```

If Tavily is configured:

```text
Research Agent
      │
      ▼
Tavily API
      │
      ▼
Live Search Results
```

If Tavily is not configured:

```text
Research Agent
      │
      ▼
Deterministic Search Simulator
```

The simulator exists so that development and testing do not require a search API.

For production research, configure Tavily or replace the search implementation with another search provider.

---

# Security

Never put API keys directly into:

```text
agent.py
tools.py
api.py
```

Never commit:

```text
.env
```

The repository's `.gitignore` excludes `.env`.

Correct:

```env
OPENAI_API_KEY=...
```

Incorrect:

```python
OPENAI_API_KEY = "sk-..."
```

---

# Running the Agent

After activating the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run:

```powershell
python agent.py
```

The default task is:

```text
Research the top 5 emerging AI trends in 2024,
analyze their potential market impact,
calculate average investment needed,
and generate a structured report.
```

---

# Expected Workflow

The application performs approximately:

```text
1. Start Research Agent

2. Identify candidate AI trends

3. Search for 2024 AI trend evidence

4. Search each individual trend

5. Search market impact

6. Search investment requirements

7. Collect sources

8. Estimate investment requirements

9. Calculate statistics

10. Validate research completeness

11. Handoff to Report Writer

12. Format final report

13. Return Markdown report
```

---

# Custom Research Task

You can also execute your own task.

Create a Python command:

```powershell
python -c "import asyncio; from agent import run_research_report; print(asyncio.run(run_research_report('Research the top AI infrastructure companies in 2024 and analyze their market impact, investment requirements, risks, and growth opportunities.')))"
```

---

# Running the API

Start FastAPI:

```powershell
uvicorn api:app --reload
```

Expected output:

```text
Uvicorn running on http://127.0.0.1:8000
```

Keep this PowerShell window running.

---

# Health Check

Open another PowerShell window.

Run:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/health" `
    -Method Get
```

Expected:

```text
status provider
------ --------
ok     openai
```

or:

```text
status provider
------ --------
ok     groq
```

---

# Research API

The main endpoint is:

```text
POST /research
```

Example PowerShell request:

```powershell
$body = @{
    task = "Research the top 5 emerging AI trends in 2024, analyze their potential market impact, calculate average investment needed, and generate a structured report."
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/research" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

$response.report
```

---

# Custom API Request

Example:

```powershell
$body = @{
    task = "Research AI cybersecurity trends in 2024. Identify five major trends, analyze market impact, estimate required investment, calculate the average investment, and provide sources."
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/research" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

$response.report
```

---

# Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can test:

```text
POST /research
```

directly from the browser.

---

# API Endpoints

## GET `/health`

Returns application status.

Example response:

```json
{
  "status": "ok",
  "provider": "openai"
}
```

---

## POST `/research`

Runs the multi-agent research workflow.

Request:

```json
{
  "task": "Research the top 5 emerging AI trends in 2024."
}
```

Response:

```json
{
  "report": "# AI Trends 2024 Research Report\n\n..."
}
```

---

# Tools

The agent has three tools.

## Tool 1 — Web Search

```python
web_search(
    query: str,
    max_results: int = 5
)
```

Purpose:

```text
Research
↓
External evidence
↓
Sources
```

It uses Tavily when configured.

---

# Tool 2 — Data Analysis

```python
calculate_statistics(
    values,
    metric="mean"
)
```

Supported metrics:

```text
mean
median
min
max
sum
```

Example:

```python
calculate_statistics(
    [100, 200, 300, 400, 500],
    "mean"
)
```

Result:

```json
{
  "metric": "mean",
  "values": [
    100,
    200,
    300,
    400,
    500
  ],
  "result": 300.0,
  "units": "USD millions"
}
```

The Research Agent uses this tool to calculate the average estimated investment.

---

# Tool 3 — Save Report

The optional file tool:

```python
save_report(
    report,
    filename="research_report.md"
)
```

It saves the report into:

```text
reports/
```

For example:

```text
reports/research_report.md
```

The filename is sanitized to prevent basic path traversal.

---

# Investment Analysis

The agent must produce five investment estimates.

Example:

```text
Trend                         Investment
------------------------------------------------
Generative AI                 $500M
AI Agents                    $250M
AI Infrastructure            $1,000M
Edge AI                      $300M
AI Cybersecurity             $200M
```

The calculation tool then calculates:

```text
Total
Average
Minimum
Maximum
```

For example:

```text
Average = (500 + 250 + 1000 + 300 + 200) / 5
        = 450 million USD
```

The actual values generated by the application depend on the research and sources available at runtime.

---

# Important Research Disclaimer

Investment figures should not automatically be interpreted as factual market data.

The agent is instructed to distinguish between:

```text
Sourced Fact
```

and:

```text
Analytical Estimate
```

For example:

```text
Source states that Company X invested $500M.
```

is a sourced fact.

Whereas:

```text
Estimated investment required to build this capability:
$250M.
```

is an analytical estimate.

The report should explain the assumptions behind estimates.

---

# Testing

Run the test suite:

```powershell
pytest -q
```

The tests are designed to run without making an LLM API request.

Expected output should resemble:

```text
6 passed
```

---

# Test Calculation Tool Manually

You can also run:

```powershell
python -c "from tools import calculate_statistics; print(calculate_statistics.__wrapped__([100,200,300,400,500]))"
```

Expected:

```json
{"metric": "mean", "values": [100.0, 200.0, 300.0, 400.0, 500.0], "result": 300.0, "units": "USD millions"}
```

---

# Error Handling

The system has two retry layers.

## Web Search Retry

The search layer retries transient failures such as:

```text
408
425
429
500
502
503
504
timeouts
network errors
```

---

# Exponential Backoff

The retry sequence approximately follows:

```text
Attempt 1
   ↓
1 second

Attempt 2
   ↓
2 seconds

Attempt 3
   ↓
4 seconds

Attempt 4
   ↓
8 seconds
```

Jitter is added to reduce synchronized retry behavior.

The maximum number of retries is controlled by:

```env
MAX_RETRIES=4
```

---

# Timeout Handling

The HTTP request timeout is configured with:

```env
REQUEST_TIMEOUT_SECONDS=30
```

For slower environments:

```env
REQUEST_TIMEOUT_SECONDS=60
```

---

# Logging

Logging is controlled with:

```env
LOG_LEVEL=INFO
```

Possible values include:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

For debugging:

```env
LOG_LEVEL=DEBUG
```

---

# Graceful Search Failure

If the search provider fails after all retries, the tool returns structured information rather than immediately crashing the entire agent workflow.

This allows the agent to continue where possible and explain limitations in the final report.

---

# GitHub Setup

Initialize Git:

```powershell
git init
```

Check status:

```powershell
git status
```

Add files:

```powershell
git add .
```

Create the initial commit:

```powershell
git commit -m "Initial AI research report agent"
```

Set main branch:

```powershell
git branch -M main
```

---

# Create GitHub Repository

Create an empty repository on GitHub named:

```text
ai-research-agent
```

Do not initialize it with another README if you already have this README locally.

Then:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/ai-research-agent.git
```

Verify:

```powershell
git remote -v
```

Push:

```powershell
git push -u origin main
```

---

# Verify Secrets Are Not Committed

Run:

```powershell
git status
```

Make sure:

```text
.env
```

is not listed.

You can also check:

```powershell
git ls-files
```

You should see:

```text
agent.py
api.py
tools.py
test_agent.py
requirements.txt
.env.example
.gitignore
render.yaml
README.md
```

You should NOT see:

```text
.env
```

---

# Render Deployment

The project contains:

```text
render.yaml
```

This defines the deployment configuration.

## Build Command

```text
pip install -r requirements.txt
```

## Start Command

```text
uvicorn api:app --host 0.0.0.0 --port $PORT
```

---

# Deploy to Render

1. Push the project to GitHub.
2. Log in to Render.
3. Create a new Blueprint/Web Service.
4. Select your GitHub repository.
5. Render reads `render.yaml`.
6. Configure environment variables.
7. Deploy.

---

# Render Environment Variables

For OpenAI:

```text
LLM_PROVIDER=openai

OPENAI_API_KEY=your_key

OPENAI_MODEL=gpt-4o-mini

TAVILY_API_KEY=your_key

MAX_RETRIES=4

REQUEST_TIMEOUT_SECONDS=30

LOG_LEVEL=INFO
```

For Groq:

```text
LLM_PROVIDER=groq

GROQ_API_KEY=your_key

GROQ_MODEL=your_model

TAVILY_API_KEY=your_key

MAX_RETRIES=4

REQUEST_TIMEOUT_SECONDS=30

LOG_LEVEL=INFO
```

---

# Verify Production Deployment

After deployment, Render will provide a URL similar to:

```text
https://your-service.onrender.com
```

Health check:

```text
https://your-service.onrender.com/health
```

API documentation:

```text
https://your-service.onrender.com/docs
```

Research endpoint:

```text
POST https://your-service.onrender.com/research
```

---

# Production API Testing

PowerShell:

```powershell
$body = @{
    task = "Research the top 5 emerging AI trends in 2024, analyze market impact, estimate investment requirements, calculate the average investment, and produce a structured report."
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "https://YOUR-RENDER-URL.onrender.com/research" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

$response.report
```

---

# Recommended Production Architecture

The first version uses synchronous HTTP execution:

```text
Client
  │
  ▼
FastAPI
  │
  ▼
Research Agent
  │
  ▼
Report Writer
  │
  ▼
HTTP Response
```

For high-volume production deployments, use asynchronous jobs:

```text
Client
  │
  ▼
POST /research
  │
  ▼
Create Job
  │
  ▼
Queue
  │
  ▼
Worker
  │
  ├── Research Agent
  │
  ├── Web Search
  │
  ├── Calculations
  │
  └── Report Writer
  │
  ▼
Database
  │
  ▼
GET /research/{job_id}
```

This avoids keeping an HTTP request open during long research operations.

---

# Supabase Integration

Supabase can optionally be added for persistent conversation and job history.

Recommended tables:

## `research_jobs`

```text
id
user_id
task
status
created_at
started_at
completed_at
report
error
```

Possible statuses:

```text
queued
running
completed
failed
```

## `agent_messages`

```text
id
research_job_id
agent_name
role
content
created_at
```

This allows you to store:

```text
User request
    ↓
Research Agent messages
    ↓
Tool results
    ↓
Handoff
    ↓
Report Writer messages
    ↓
Final report
```

Supabase is intentionally not required by the base project so that the core agent remains easy to run locally.

---

# Troubleshooting

## Problem: Python Not Found

Run:

```powershell
py --version
```

If Python is installed:

```powershell
py -3.11 --version
```

Create the environment with:

```powershell
py -3.11 -m venv .venv
```

---

# Problem: PowerShell Cannot Activate Virtual Environment

Error:

```text
running scripts is disabled on this system
```

Run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

# Problem: `OPENAI_API_KEY` Error

If you see:

```text
OPENAI_API_KEY is required
```

check `.env`:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
```

Then restart the Python process.

---

# Problem: Groq API Error

Check:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_key
GROQ_MODEL=your_supported_model
```

Make sure the selected model is currently available through your Groq account.

---

# Problem: Search Uses Simulator

If logs contain:

```text
TAVILY_API_KEY not configured.
Using simulated search results.
```

then configure:

```env
TAVILY_API_KEY=your_key
```

Restart the application.

---

# Problem: Rate Limit

If you receive:

```text
429
```

the application automatically retries transient failures.

You can adjust:

```env
MAX_RETRIES=5
```

However, retries do not increase your provider quota.

For sustained high traffic, implement:

* request throttling
* concurrency limits
* queues
* provider quota management
* caching

---

# Problem: Request Timeout

Increase:

```env
REQUEST_TIMEOUT_SECONDS=60
```

Restart:

```powershell
uvicorn api:app --reload
```

For production workloads with long research jobs, use an asynchronous job architecture.

---

# Problem: `ModuleNotFoundError`

Make sure the virtual environment is activated:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then:

```powershell
pip install -r requirements.txt
```

Check:

```powershell
pip list
```

---

# Problem: Agent Does Not Handoff

Check `agent.py`.

The Research Agent must contain:

```python
handoffs=[
    handoff(report_writer_agent)
]
```

The research instructions must also tell the model to hand off after completing its research.

The final output should be produced by:

```text
Report Writer Agent
```

not directly by the Research Agent.

---

# Problem: Calculation Fails

The calculation tool requires:

```text
at least one numeric value
```

Values must also be finite numbers.

Valid:

```python
[100, 200, 300]
```

Invalid:

```python
[]
```

or:

```python
[100, float("nan")]
```

---

# Problem: `.env` Appears in Git

Immediately remove it from Git tracking:

```powershell
git rm --cached .env
```

Then commit:

```powershell
git commit -m "Remove environment secrets"
```

If the API key was already pushed to GitHub, rotate/revoke that API key immediately.

---

# Development Workflow

Recommended development workflow:

```text
1. Activate virtual environment

2. Modify code

3. Run unit tests

4. Run local agent

5. Start FastAPI

6. Test /health

7. Test /research

8. Commit changes

9. Push GitHub

10. Deploy Render
```

Commands:

```powershell
.\.venv\Scripts\Activate.ps1

pytest -q

python agent.py

uvicorn api:app --reload
```

---

# Complete Windows Command Sequence

For a fresh machine:

```powershell
New-Item -ItemType Directory -Path "ai-research-agent" -Force

Set-Location "ai-research-agent"

py -3.11 -m venv .venv

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

pip install -r requirements.txt

Copy-Item .env.example .env

notepad .env

pytest -q

python agent.py
```

Then start the API:

```powershell
uvicorn api:app --reload
```

---

# API Test Sequence

In another PowerShell window:

```powershell
Set-Location "ai-research-agent"

.\.venv\Scripts\Activate.ps1
```

Health check:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/health" `
    -Method Get
```

Research:

```powershell
$body = @{
    task = "Research the top 5 emerging AI trends in 2024, analyze their potential market impact, calculate average investment needed, and generate a structured report."
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/research" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

$response.report
```

---

# Production Checklist

Before deploying publicly:

* [ ] `.env` is not committed
* [ ] API keys stored as environment variables
* [ ] OpenAI or Groq provider tested
* [ ] Tavily configured
* [ ] Unit tests passing
* [ ] `/health` working
* [ ] `/research` working
* [ ] Retry handling tested
* [ ] Timeout handling tested
* [ ] Rate-limit behavior tested
* [ ] Logs enabled
* [ ] API authentication added
* [ ] API rate limiting added
* [ ] Request size limits configured
* [ ] Background jobs considered for long research
* [ ] Persistent storage configured if required
* [ ] Secrets configured in Render
* [ ] Production URL tested

---

# Security Recommendations

For a public production API, add authentication.

Do not expose an unauthenticated research endpoint indefinitely.

Recommended architecture:

```text
Client
  │
  ▼
Authentication
  │
  ▼
Rate Limiter
  │
  ▼
FastAPI
  │
  ▼
Agent
```

Also consider:

* API keys or JWT
* per-user quotas
* request logging
* abuse prevention
* maximum prompt size
* concurrency limits
* cost controls
* output limits
* monitoring

---

# Cost Control

AI research can generate multiple model calls and search requests.

The Research Agent may perform:

```text
Multiple web searches
        +
Multiple LLM calls
        +
Tool calls
        +
Report generation
```

Therefore, production systems should monitor:

```text
Requests/day
LLM tokens/request
Searches/request
Average latency
Failure rate
Cost/request
```

Useful controls include:

```env
MAX_RETRIES=4
```

and application-level:

```text
maximum concurrent requests
maximum research steps
maximum output length
maximum searches
```

---

# Observability

At minimum monitor:

```text
Agent execution time
Search latency
LLM latency
Number of tool calls
Number of retries
429 responses
5xx responses
Workflow failures
```

For production, integrate your preferred logging/monitoring provider.

---
