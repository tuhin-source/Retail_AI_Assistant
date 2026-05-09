from data_loader import products
from data_loader import policy 
from data_loader import orders
import json
import ast

def search_products(filters):
   df = products.copy()

   if "tags" in filters:
      for tag in filters["tags"]:
          df = df[df["tags"].str.contains(tag, case=False)]
   
   if "size" in filters:
      size = str(filters["size"])
      def size_in_stock(row):
          stock = ast.literal_eval(row["stock_per_size"])
          return stock.get(size, 0)>0
      df = df[df.apply(size_in_stock, axis=1)]
    
   if "max_price" in filters:
      df = df[df["price"] <= filters["max_price"]]
   
   df = df.sort_values("bestseller_score", ascending=False)
   return {"total_found": len(df), "products": df.head(5).to_dict(orient="records")}

def get_product(product_id):
    match = products[products["product_id"] == product_id]
    
    if match.empty:
        return {"error": f"Product '{product_id}' not found"}
    
    return {"product": match.iloc[0].to_dict()}

def get_order(order_id):
    match = orders[orders["order_id"].astype(str) == str(order_id)]
    
    if match.empty:
        return {"error": f"Order '{order_id}' not found"}
    
    return {"order": match.iloc[0].to_dict()}

from datetime import date, datetime

def evaluate_return(order_id):
    order_result = get_order(order_id)
    if "error" in order_result:
        return {"decision": "REJECTED", "reason": order_result["error"]}

    order = order_result["order"]
    product_result = get_product(order["product_id"])
    if "error" in product_result:
        return {"decision": "REJECTED", "reason": product_result["error"]}

    product = product_result["product"]

    order_date = datetime.strptime(str(order["order_date"]), "%Y-%m-%d").date()
    days_since = (date.today() - order_date).days

    if product["is_clearance"]:
        return {"decision": "REJECTED", "reason": "Clearance items are final sale."}

    if product["vendor"] == "Aurelia Couture":
        return {"decision": "APPROVED", "reason": "Aurelia Couture: exchanges only.", "refund_type": "exchange only"}

    if product["is_sale"]:
        if days_since <= 7:
            return {"decision": "APPROVED", "reason": f"Sale item, {days_since} days since purchase.", "refund_type": "store credit only"}
        else:
            return {"decision": "REJECTED", "reason": f"Sale return window is 7 days. Been {days_since} days."}

    window = 21 if product["vendor"] == "Nocturne" else 14

    if days_since <= window:
        return {"decision": "APPROVED", "reason": f"Within {window}-day window ({days_since} days).", "refund_type": "full refund"}
    else:
        return {"decision": "REJECTED", "reason": f"Window is {window} days. Been {days_since} days."}

if __name__ == "__main__":
    print(search_products({"tags": ["flowy"], "size": "8"}))
    print(get_product("P0001"))
    print(get_order("O0001"))
    print(evaluate_return("O0001"))
    print(evaluate_return("O9999"))  # invalid order