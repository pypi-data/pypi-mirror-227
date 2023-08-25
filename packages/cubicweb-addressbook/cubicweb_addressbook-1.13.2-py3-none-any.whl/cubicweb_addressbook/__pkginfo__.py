# pylint: disable-msg=W0622
"""cubicweb-addressbook packaging information"""

modname = 'addressbook'
distname = "cubicweb-%s" % modname

numversion = (1, 13, 2)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
description = "address book component for the CubicWeb framework"
author = "Logilab"
author_email = "contact@logilab.fr"
web = 'https://forge.extranet.logilab.fr/cubicweb/cubes/%s' % distname
classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]

__depends__ = {'cubicweb': ">= 3.38.0, < 3.39.0",
               'cubicweb-geocoding': None,
               }
