# -*- coding: utf-8 -*-
{
    'name': "in_memory_filestore",

    'summary': """
        Change the filestore to in memory. Only for testing (CI) purposes.""",

    'description': """
        This module changes the filestore to in memory. The goal is to use it
        to save time in the CI process. It is not intended to be used in
        production.
    """,

    'author': "Coopdevs",
    'website': "http://www.coopdevs.org",
    'category': 'Technical',
    'version': '12.0.1.0.1',


    'depends': ['base'],

    'data': [
        'data/ir_config_parameter.xml',
    ],
}
