{
    "name": "Online Quote",
    "version": "1.0",
    "category": "Sales",
    "license": "LGPL-3",
    "summary": "Custom module for online quotation management",
    "description": """
        A module to manage online quotations with properties like 
        Property Type, Sub Property Types, Number of Rooms, and more.
    """,
    "author": "Abenezer Nigussie",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/onquote_view.xml",
    ],
    "installable": True,
    "application": True,
}
