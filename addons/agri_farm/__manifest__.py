{
    'name': 'Agriculture Farm Management',
    'version': '1.0',
    'summary': 'Farm and Field management layer for B3agric ERP',
    'description': """
        Custom farm-management layer: Farm -> Field.
        Feeds into existing Inventory/Manufacturing/Sales for
        harvest, storage, spoilage, processing, and sale.
    """,
    'author': 'B3agric',
    'category': 'Agriculture',
    'depends': ['base', 'product', 'stock', 'product_expiry'],
    'data': [
        'security/ir.model.access.csv',
        'views/farm_views.xml',
        'views/field_views.xml',
        'views/crop_views.xml',
        'views/planting_views.xml',
        'views/harvest_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
