import unittest
from src.discovery.digital_link import DigitalLink, DigitalLinkParser

class TestDigitalLink(unittest.TestCase):
    def test_parser_with_canonical_link(self):
        uri = "https://id.brand.com/01/1234567890123/10/BATCH123/21/SERIAL456"
        parser = DigitalLinkParser()
        parsed = parser.parse_uri(uri)
        self.assertEqual(parsed.get('01'), '1234567890123')
        self.assertEqual(parsed.get('10'), 'BATCH123')
        self.assertEqual(parsed.get('21'), 'SERIAL456')

    def test_digital_link_class_parsing(self):
        uri = "https://id.brand.com/01/1234567890123/10/BATCH123"
        resolver = DigitalLink(uri)
        parsed = resolver.parse()
        self.assertEqual(parsed.get('01'), '1234567890123')
        self.assertEqual(parsed.get('gtin'), '1234567890123')
        self.assertEqual(parsed.get('10'), 'BATCH123')
        self.assertEqual(parsed.get('batch'), 'BATCH123')
        self.assertIsNone(parsed.get('serial'))

    def test_digital_link_routing(self):
        uri = "https://id.brand.com/01/1234567890123/10/BATCH123"
        resolver = DigitalLink(uri)
        route_info = resolver.route()
        self.assertIn("application/ld+json", route_info["acceptable_headers"])
        self.assertEqual(route_info["redirection_links"]["gs1:pip"], "https://id.brand.com/01/1234567890123/info")
        self.assertEqual(route_info["redirection_links"]["gs1:dpp"], "https://id.brand.com/01/1234567890123/dpp")
        self.assertEqual(route_info["redirection_links"]["gs1:certificationInfo"], "https://id.brand.com/01/1234567890123/certinfo")

if __name__ == '__main__':
    unittest.main()
