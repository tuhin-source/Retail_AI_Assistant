from google import genai
from google.genai import types
import json
import os
from tools import search_products, get_product, get_order, evaluate_return
from tool_schemas import TOOL_SCHEMAS

client = genai.Client(api_key="Paste_Your_Gemini_Api_Key")

SYSTEM_PROMPT = """You are a retail AI assistant with two jobs:
1. PERSONAL SHOPPER — Help customers find dresses based on style, size, budget.
2. CUSTOMER SUPPORT — Handle return and refund requests using policy rules.

Rules:
- Always use tools to get data. Never guess product names, prices or order details.
- If order is not found, say so clearly.
- When recommending products, explain WHY it matches what they asked for.
- When handling returns, state clearly APPROVED or REJECTED and why.
"""

TOOL_FUNCTIONS = {
    "search_products": search_products,
    "get_product": get_product,
    "get_order": get_order,
    "evaluate_return": evaluate_return
}

conversation = []

def run_agent(user_message):
    conversation.append(types.Content(
        role="user",
        parts=[types.Part(text=user_message)]
    ))

    while True:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[TOOL_SCHEMAS]
            )
        )

        # Check if Gemini wants to call a tool
        tool_calls = []
        for part in response.candidates[0].content.parts:
            if hasattr(part, "function_call") and part.function_call:
                tool_calls.append(part.function_call)

        # No tool calls — return final answer
        if not tool_calls:
            final_text = response.candidates[0].content.parts[0].text
            conversation.append(response.candidates[0].content)
            return final_text

        # Add Gemini's tool request to conversation
        conversation.append(response.candidates[0].content)

        # Run each tool
        tool_results = []
        for call in tool_calls:
            name = call.name
            args = dict(call.args)
            print(f"\n  [Tool Call] {name}({args})")

            if name == "search_products":
                result = search_products(args)
            elif name == "get_product":
                result = get_product(args["product_id"])
            elif name == "get_order":
                result = get_order(args["order_id"])
            elif name == "evaluate_return":
                result = evaluate_return(args["order_id"])

            print(f"  [Tool Result] {json.dumps(result, default=str)[:200]}")

            tool_results.append(types.Part(
                function_response=types.FunctionResponse(
                    name=name,
                    response={"result": json.dumps(result, default=str)}
                )
            ))

        # Send tool results back
        conversation.append(types.Content(
            role="user",
            parts=tool_results
        ))