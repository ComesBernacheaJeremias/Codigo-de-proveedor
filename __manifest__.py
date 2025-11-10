{
    "name": "Product Extended Fields",
    "version": "18.0.1.0.0",
    "depends": ["product"],
    "author": "ChatGPT",
    "category": "Product",
    "description": "Adds supplier code and brand fields to product.template and enables searching by them.",
    "data": [
        "views/product_template_views.xml",
        "views/product_template_search.xml",
        "views/product_product_views.xml",
        "security/ir.model.access.csv"
    ],
    "installable": True,
    "license": "AGPL-3",
}