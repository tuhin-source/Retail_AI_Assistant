# Retail AI Assistant — Architecture Document

## Overview

A single conversational AI agent powered by Google Gemini 2.0 Flash that handles two retail roles:
**Personal Shopper** (revenue) and **Customer Support** (operations).
Built with the `google-genai` Python SDK's native tool/function calling.

---

## 1. Why I Structured the Agent This Way

### One Agent, Two Roles

Rather than building two separate agents, a single agent with a well-crafted system prompt
handles both roles. The system prompt defines clear behavior rules for each mode, and Gemini
routes itself based on the user's intent.

This approach has three advantages:
- A customer can ask about a product and then ask about a return in the same conversation
- Conversation history is unified — no coordination between agents needed
- Simpler codebase — one agent loop, one system prompt, one set of tools

### Layered Architecture

```
main.py          ← CLI loop, user input/output
agent.py         ← system prompt, agentic loop, Gemini API calls
tools.py         ← 4 tool functions (pure Python, no AI)
tool_schemas.py  ← tells Gemini what tools exist and what arguments they take
data_loader.py   ← loads CSV and policy files into memory
data/            ← product_inventory.csv, orders.csv, policy.txt
```

Each layer has one job. Tools have no knowledge of Gemini. The agent has no knowledge
of CSVs. This separation makes each component independently testable and easy to debug.

### Agentic Loop

```
User types message
       ↓
Gemini reads message + decides which tool to call
       ↓
Python runs the tool against real CSV data
       ↓
Result is sent back to Gemini
       ↓
Gemini reasons over the result and responds
```

The loop continues until Gemini stops calling tools and returns a final text response.

---

## 2. How Hallucination Is Minimized

### Tools Are the Only Source of Truth

The system prompt contains an explicit instruction:
"Always use tools to get data. Never guess product names, prices or order details."

Gemini cannot invent a product or order — it must call a tool first. If the tool
returns an error (product not found, order not found), Gemini is instructed to
relay that error to the customer rather than substitute alternative information.

### Error Propagation

`get_order` and `get_product` return structured `{"error": "..."}` responses when
data is not found. Gemini surfaces these errors directly to the user. An invalid
order ID always results in a clear "not found" message — never a guess.

### Policy Applied in Code, Not by Gemini

`evaluate_return` applies all policy rules deterministically in Python:
- Clearance check
- Sale window (7 days)
- Vendor exceptions (Aurelia Couture, Nocturne)
- Standard window (14 days)

Gemini reads the decision and explains it. It does not re-derive policy from memory.
This eliminates the risk of Gemini misremembering or misapplying policy rules.

### Stock Verification at the Data Layer

`search_products` filters out products with zero stock for the requested size
before returning results. Gemini never sees out-of-stock products for the
requested size, eliminating the risk of recommending unavailable items.

---

## 3. How Tools Are Selected

Gemini uses the tool descriptions in `tool_schemas.py` to decide when and which
tool to call. The descriptions are written to be unambiguous:

| Situation | Tool Selected |
|---|---|
| Customer describes what they want to buy | `search_products` with extracted filters |
| Agent needs details on one specific product | `get_product` |
| Customer mentions an order number | `get_order` |
| Customer asks about returning an order | `evaluate_return` |

Gemini can chain tools within a single turn if needed. For example, it can call
`search_products` to find options and then `get_product` to verify a specific detail
before responding — all without any hardcoded routing logic.

---

## 4. Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| AI Model | Gemini 2.0 Flash |
| AI Client | google-genai (official Google SDK) |
| Data | pandas (CSV querying) |
| Interface | CLI (input/output loop) |
| Data files | CSV (products, orders), TXT (policy) |

No external frameworks, no database, no web server.
The system is intentionally minimal so that agent reasoning quality is the focus.

---

## 5. Key Design Decisions

**Why Gemini 2.5 Flash?**
Fast, capable of multi-turn tool calling, and cost-effective for a simulation project.

**Why pandas over a database?**
The dataset is small and static. Pandas loads everything into memory at startup,
making queries fast with no infrastructure overhead.

**Why one policy file instead of hardcoded rules?**
Keeping policy in a text file makes it easy to update rules without touching code.
The `evaluate_return` function reads and applies these rules programmatically.

**Why not LangChain?**
Gemini's native tool calling handles the entire agentic loop. LangChain would add
unnecessary abstraction, making the system harder to debug and explain.
