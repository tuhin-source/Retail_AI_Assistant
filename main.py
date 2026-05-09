from agent import run_agent

print("🛍️  Retail AI Assistant")
print("Type 'quit' to exit\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "quit":
        break
    if not user_input:
        continue
    print("\n[Thinking...]\n")
    reply = run_agent(user_input)
    print(f"Assistant: {reply}\n")