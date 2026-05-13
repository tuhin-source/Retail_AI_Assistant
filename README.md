# Retail AI Assistant

A conversational AI agent that acts as both a Personal Shopper and Customer Support Assistant for a fashion retail store.

## What it does

- Recommends products based on size, style, budget and sale preference
- Handles return and refund requests using real policy rules
- Uses tool calling — never guesses or makes up data

## Project Structure

```
Retail_AI_Assistant/
│
├── data/
│   ├── product_inventory.csv
│   ├── orders.csv
│   └── policy.txt
│
├── data_loader.py     # loads CSV and policy files
├── tools.py           # 4 tool functions
├── tool_schemas.py    # tool definitions for Gemini
├── agent.py           # agent loop + Gemini API
└── main.py            # CLI entrypoint
```

## Setup

### 1. Clone the repository
```
git clone <your-repo-link>
cd Retail_AI_Assistant
```

### 2. Install dependencies
```
pip install google-genai pandas
```

### 3. Add your Gemini API key

Open agent.py and replace this line:

```python
client = genai.Client(api_key="YOUR_GEMINI_API_KEY_HERE")
```

With your actual key from https://aistudio.google.com

### 4. Run
```
python main.py
```

## Example Interactions

Shopping:
```
You: I need a flowy dress under $300 in size 8
You: Show me modest evening dresses on sale in size 10
```

Returns:
```
You: I want to return order O0001
You: Can I return order O9999
```

## Tools

| Tool | Purpose |
|---|---|
| search_products | Filter products by tags, size, price, sale status |
| get_product | Fetch one product by ID |
| get_order | Fetch one order by ID |
| evaluate_return | Apply return policy and give APPROVED or REJECTED |

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.12+ |
| AI Model | Gemini 2.5 Flash |
| AI Client | google-genai |
| Data | pandas |
| Interface | CLI |
