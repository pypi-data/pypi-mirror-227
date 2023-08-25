import unittest
from cubicweb_web.devtools.testlib import AutomaticWebTest


class AddressbookAutomaticWebTest(AutomaticWebTest):
    def to_test_etypes(self):
        return {"PhoneNumber", "PostalAddress"}

    def list_startup_views(self):
        return ()


del AutomaticWebTest

if __name__ == "__main__":
    unittest.main()
