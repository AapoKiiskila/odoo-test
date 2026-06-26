{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "TestUser",
    'application': True,
    'data': [
      'security/ir.model.access.csv',

      'views/real_estate_property_views.xml',
      'views/real_estate_property_offer_views.xml',
      'views/real_estate_property_type_views.xml',
      'views/real_estate_property_tag_views.xml',
      'views/res_users_views.xml',
      'views/real_estate_menus.xml'
    ]
}
