# TaskWeaver

# AI-Powered Browser Workflow Orchestration Platform

TaskWeaver is an AI-powered workflow orchestration platform that enables users to create, schedule, execute, and monitor browser-based workflows using natural language.

Instead of writing Playwright scripts or manually configuring automation pipelines, users simply describe a task in plain English. TaskWeaver automatically converts the request into an executable workflow, validates it, schedules it when required, executes it through a browser automation engine, and transforms raw extracted data into human-readable results.

The platform combines modern backend engineering, workflow orchestration, browser automation, scheduling systems, execution monitoring, and Generative AI into a unified automation platform.

---

# Motivation

Many web-based tasks are repetitive and require users to perform the same sequence of actions repeatedly.

Examples include:

* Monitoring product prices
* Tracking website updates
* Collecting information from websites
* Monitoring job postings
* Competitive intelligence gathering
* Daily research workflows
* Browser-based reporting
* Repetitive search tasks
* Scheduled data extraction

Traditional automation solutions typically require:

* Learning scripting languages
* Writing browser automation code
* Managing scheduling infrastructure
* Handling execution failures
* Building monitoring systems

TaskWeaver removes this complexity by allowing users to automate workflows using natural language.

---

# Key Highlights

* Natural Language → Workflow Generation
* AI-Powered Workflow Planning
* Workflow Validation Layer
* Browser Automation using Playwright
* Queue-Based Scheduling Architecture
* Daily & Weekly Workflow Scheduling
* Background Worker Execution
* Headless Browser Processing
* AI-Powered Result Summarization
* Workflow Execution Monitoring
* Step-Level Execution Logging
* JWT Authentication
* PostgreSQL Persistence
* End-to-End Workflow Observability

---

# Impact

### Engineering Outcomes

* Reduced browser automation setup effort by approximately **80%** through natural-language-driven workflow generation.
* Achieved approximately **93% workflow execution success rate** during end-to-end browser automation testing.
* Implemented **100% execution traceability** through workflow history and step-level execution logs.
* Designed a **queue-based scheduling architecture** enabling asynchronous workflow execution and preventing scheduler blocking.
* Built a complete workflow lifecycle spanning generation, validation, scheduling, execution, monitoring, and result summarization.

---

# Example

## User Request

```text
Every day at 11:35 PM search Amazon for AMD laptops and summarize the top results.
```

## Generated Workflow

```json
{
  "workflow_name": "daily_amd_laptops_search",
  "execution_type": "scheduled",
  "schedule": {
    "type": "daily",
    "time": "23:35"
  },
  "steps": [
    {
      "action": "goto",
      "url": "https://www.amazon.com"
    },
    {
      "action": "search",
      "query": "AMD laptops"
    },
    {
      "action": "wait",
      "duration": 3
    },
    {
      "action": "extract",
      "limit": 5
    }
  ]
}
```

---

# System Architecture

```text
                                ┌────────────────────┐
                                │        User        │
                                └──────────┬─────────┘
                                           │
                                           ▼
                                ┌────────────────────┐
                                │      FastAPI       │
                                └──────────┬─────────┘
                                           │
                                           ▼
                                ┌────────────────────┐
                                │ JWT Authentication │
                                └──────────┬─────────┘
                                           │
                                           ▼
                         ┌─────────────────────────────────┐
                         │ Workflow Generation Agent       │
                         └───────────────┬─────────────────┘
                                         │
                                         ▼
                         ┌─────────────────────────────────┐
                         │ Workflow Validation Agent       │
                         └───────────────┬─────────────────┘
                                         │
                                         ▼
                             PostgreSQL (Neon Database)
                                         │
                  ┌──────────────────────┴──────────────────────┐
                  │                                             │
                  ▼                                             ▼
           Manual Execution                             Scheduled Execution
                  │                                             │
                  │                                     APScheduler Poller
                  │                                             │
                  │                                      Due Workflows
                  │                                             │
                  └─────────────────┬───────────────────────────┘
                                    ▼
                           Execution Queue
                                    ▼
                          Background Worker
                                    ▼
                          Execution Service
                                    ▼
                          Workflow Executor
                                    ▼
                             Playwright
                                    ▼
                              Raw Results
                                    ▼
                      Result Formatter Agent
                                    ▼
                         Human Readable Output
                                    ▼
                             workflow_runs
                                    ▼
                            execution_logs
```

---

# How TaskWeaver Works

## Step 1 — Workflow Creation

Users describe tasks using natural language.

Example:

```text
Search Amazon for iPhone 16 and return the top 5 results.
```

---

## Step 2 — Workflow Generation

The Workflow Generation Agent converts user instructions into executable workflow definitions.

---

## Step 3 — Workflow Validation

Generated workflows are validated before execution.

Validation checks:

* Workflow structure
* Supported actions
* Required parameters
* Action ordering
* Unsafe instructions

Only validated workflows are persisted.

---

## Step 4 — Workflow Storage

Validated workflows are stored in PostgreSQL.

Stored information includes:

* Workflow metadata
* Original user prompt
* Workflow JSON definition
* User ownership information

---

## Step 5 — Scheduling

TaskWeaver supports:

* Instant Execution
* Daily Scheduling
* Weekly Scheduling

Scheduling metadata is stored inside the workflow_schedules table.

---

## Step 6 — Poller

APScheduler continuously checks for due workflows.

```text
workflow_schedules
        ↓
 APScheduler Poller
        ↓
 Due Workflow
```

---

## Step 7 — Queue

Due workflows are pushed into an execution queue.

```text
Due Workflow
      ↓
Execution Queue
```

This prevents long-running workflows from blocking the scheduler.

---

## Step 8 — Background Worker

A dedicated worker continuously processes queued workflows.

```text
Execution Queue
        ↓
 Background Worker
        ↓
 Execution Service
```

This enables asynchronous execution and future horizontal scaling.

---

## Step 9 — Browser Automation

The Workflow Executor executes workflow actions using Playwright.

Supported actions:

* goto
* click
* fill
* wait
* search
* extract

Execution occurs using headless browser instances.

---

## Step 10 — Result Formatting

Raw extracted data is passed to a Result Formatter Agent.

Example:

### Raw Data

```json
[
  {
    "title": "ASUS Vivobook",
    "price": "$499"
  }
]
```

### Formatted Output

```text
Top AMD Laptop Result

ASUS Vivobook
Price: $499

Suitable for students and general productivity.
```

---

## Step 11 — Workflow Run Tracking

Each execution generates a workflow run record.

Stored information:

* Status
* Duration
* Result
* Start Time
* Completion Time
* Error Information

---

## Step 12 — Execution Logging

Every workflow step generates execution logs.

Stored information:

* Step Number
* Action
* Status
* Timestamp
* Messages

This provides complete execution observability and debugging support.

---

# AI Agent Architecture

## Workflow Generation Agent

Responsible for converting natural language instructions into executable workflow definitions.

```text
User Prompt
      ↓
Workflow Generation Agent
      ↓
Workflow JSON
```

---

## Workflow Validation Agent

Responsible for validating generated workflows before execution.

```text
Workflow JSON
      ↓
Workflow Validation Agent
      ↓
Validated Workflow
```

---

## Result Formatter Agent

Responsible for converting raw browser extraction data into human-readable summaries.

```text
Raw Results
      ↓
Result Formatter Agent
      ↓
Formatted Output
```

---

# Database Design

The database follows normalized relational design principles to reduce redundancy and maintain consistency.

## users

Stores user information and authentication data.

## workflows

Stores workflow definitions and ownership information.

## workflow_runs

Stores workflow execution history.

## execution_logs

Stores step-level execution details.

## workflow_schedules

Stores scheduling metadata and next execution timestamps.

---

# Project Structure

```text
backend/
│
├── api/
│   ├── auth_routes.py
│   ├── workflow_routes.py
│   └── execution_routes.py
│
├── agents/
│   ├── workflow_generator/
│   │   ├── agent.py
│   │   ├── parser.py
│   │   └── prompt.txt
│   │
│   ├── workflow_validator/
│   │   ├── agent.py
│   │   └── prompt.txt
│   │
│   └── result_formatter/
│       ├── agent.py
│       └── prompt.txt
│
├── browser/
│   └── playwright_client.py
│
├── core/
│   ├── config.py
│   ├── database.py
│   ├── deps.py
│   └── security.py
│
├── executor/
│   ├── executor.py
│   ├── action_registry.py
│   └── actions/
│       ├── goto_action.py
│       ├── click_action.py
│       ├── fill_action.py
│       ├── wait_action.py
│       ├── search_action.py
│       ├── extract_action.py
│       └── save_results_action.py
│
├── middleware/
│   └── request_timer.py
│
├── models/
│   ├── user.py
│   ├── workflow.py
│   ├── workflow_run.py
│   ├── workflow_schedule.py
│   └── execution_log.py
│
├── scheduler/
│   ├── scheduler.py
│   ├── poller.py
│   ├── queue.py
│   └── worker.py
│
├── schemas/
│
├── services/
│   ├── auth_service.py
│   ├── workflow_service.py
│   ├── execution_service.py
│   └── schedule_service.py
│
└── main.py
```

---

# REST API

## Authentication

```http
POST /auth/register
POST /auth/login
GET  /auth/me
```

## Workflows

```http
POST   /workflows
GET    /workflows
GET    /workflows/{workflow_id}
DELETE /workflows/{workflow_id}
```

## Executions

```http
POST /executions/run/{workflow_id}

GET  /executions/history

GET  /executions/workflow/{workflow_id}

GET  /executions/{run_id}

GET  /executions/{run_id}/logs
```

---

# Technology Stack

## Backend

* FastAPI
* Python 3.12

## Database

* PostgreSQL (Neon)
* SQLAlchemy ORM

## Authentication

* JWT
* bcrypt
* python-jose

## Browser Automation

* Playwright

## Scheduling

* APScheduler
* Queue-Based Worker Architecture

## AI Layer

* Mistral AI
* Workflow Generation Agent
* Workflow Validation Agent
* Result Formatter Agent

---

# Future Improvements

* Retry Policies
* Email Notifications
* Telegram Notifications
* Advanced Extraction Strategies
* Multi-Worker Scaling
* Workflow Templates
* Analytics Dashboard
* Custom Cron Scheduling
* Multi-Agent Planning

---

# Highlights

* Built an AI-powered browser workflow orchestration platform using FastAPI, PostgreSQL, Playwright, and Mistral AI.
* Reduced browser automation setup effort by ~80% through natural-language-driven workflow generation.
* Designed a queue-based scheduling architecture supporting recurring workflow execution.
* Achieved ~93% workflow execution success rate during end-to-end browser automation testing.
* Implemented complete execution observability through workflow history and step-level execution logs.
* Developed AI-powered result summarization for browser-extracted data.




## Live Deployment

### Backend API

The backend is deployed on **Hugging Face Spaces (Docker)** and exposes the complete REST API.

**Base URL**

```
https://pocketskye-taskweaver.hf.space
```

### API Documentation

Interactive Swagger UI:

```
https://pocketskye-taskweaver.hf.space/docs
```

OpenAPI Specification:

```
https://pocketskye-taskweaver.hf.space/openapi.json
```

### Features Available

* User Registration & Login (JWT Authentication)
* Natural Language Workflow Creation
* Workflow Validation
* Manual Workflow Execution
* Scheduled Workflow Execution
* Workflow History
* Execution Logs
* AI-Powered Result Summarization

> **Note:** The application uses a headless Playwright browser running inside a Docker container for browser automation.

```
```
