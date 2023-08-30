from collections import namedtuple
import inspect
import unittest
from unittest.mock import MagicMock

import bs4

from crossref_citedby_driver import CrossrefCitedByClient

from .variables import (
    mock_response,
    test_xml,
    xml_filepath,
)


test_client = CrossrefCitedByClient(tech_email='support@crossref.org')


class CrossRefDriverTest(unittest.TestCase):
    """Run unit tests for the crossref cited-by driver module."""
    def setUp(self):
        with open(xml_filepath, 'r') as f:
            self.raw_data = f.read()

        self.maxDiff = None

    def test_get_crossref_citations(self) -> None:
        """Test the result is correctly extracted from the xml."""
        citations = test_client.get_crossref_citations(
            self.raw_data,
            '12.3456789/2012.12.006'
        )
        self.assertEqual(
            str(next(iter(citations.values()))[0]),            
            inspect.cleandoc(test_xml)
        )
    
    def test_get_citation_data_and_determine_timestamp(self) -> None:
        """The get citation data method returns the expected values."""
        Citation = namedtuple('Citation', ['cited_by', 'timestamp'])
        citation_entry = bs4.BeautifulSoup(
            (
                '<journal_cite>'
                '   <doi type="journal_article">12.3456789/test.2023</doi>'
                '   <year>2022</year>'
                '</journal_cite>'
            ),
            features="xml"
        )
        test_client.query_crossref_doi = MagicMock(
            return_value=mock_response
        )
        returned = test_client.get_citation_data(citation_entry)
        self.assertEqual(
            returned,
            Citation(
                cited_by='12.3456789/test.2023',
                timestamp='2022-01-01 00:00:00'
            )
        )
