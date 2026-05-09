import pandas as pd

products = pd.read_csv("C:/Agent_Projects/Retail_AI_Assistant/data/product_inventory.csv")
orders   = pd.read_csv("C:/Agent_Projects/Retail_AI_Assistant/data/orders.csv")
policy = open("C:/Agent_Projects/Retail_AI_Assistant/data/policy.txt", "r", encoding="utf8")
policy = policy.read()
# print(policy.read())
# print(products.head())