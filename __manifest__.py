{
    'name': 'Stock Analytic Extension',
    'version': '1.0',
    'category': 'Warehouse',
    'author': 'I+D, Diego Gajardo, Camilo Neira, Diego Morales',
    'website': 'https://www.holdconet.com',
    'depends': ['stock', 'account', 'analytic'],
    'data': [
        'views/stock_picking_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
}
