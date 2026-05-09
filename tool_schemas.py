from google.genai import types

TOOL_SCHEMAS = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="search_products",
            description="Search for products based on what the customer wants.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "tags": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING), description="Style tags like evening, flowy, lace"),
                    "size": types.Schema(type=types.Type.STRING, description="Size like 8, 10, 14"),
                    "max_price": types.Schema(type=types.Type.NUMBER, description="Maximum price"),
                    "is_sale": types.Schema(type=types.Type.BOOLEAN, description="True for sale items only")
                }
            )
        ),
        types.FunctionDeclaration(
            name="get_product",
            description="Get one product by its ID.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "product_id": types.Schema(type=types.Type.STRING, description="Like P0001")
                },
                required=["product_id"]
            )
        ),
        types.FunctionDeclaration(
            name="get_order",
            description="Look up a customer order by order ID.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "order_id": types.Schema(type=types.Type.STRING, description="Like O0001")
                },
                required=["order_id"]
            )
        ),
        types.FunctionDeclaration(
            name="evaluate_return",
            description="Check if an order can be returned. Use when customer asks about returns or refunds.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "order_id": types.Schema(type=types.Type.STRING, description="Like O0001")
                },
                required=["order_id"]
            )
        )
    ]
)