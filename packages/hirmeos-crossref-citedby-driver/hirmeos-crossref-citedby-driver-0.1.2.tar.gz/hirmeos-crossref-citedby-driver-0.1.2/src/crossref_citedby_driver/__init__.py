from collections import defaultdict, namedtuple
from dataclasses import dataclass, field
from logging import getLogger
import sys
from typing import Tuple

import bs4
from bs4 import BeautifulSoup
import requests
from requests.models import Response


logger = getLogger(__name__)
Citation = namedtuple('Citation', ['cited_by', 'timestamp'])


@dataclass
class CrossrefCitedByClient:

    tech_email: str
    cited_by_endpoint: str = field(
        default='https://doi.crossref.org/servlet/getForwardLinks'
    )

    def fetch_citation_xml(
            self,
            username: str,
            password: str,
            doi_prefix: str,
            start_date: str,
            end_date: str,
            api_url='https://doi.crossref.org/servlet/getForwardLinks'
    ) -> Tuple[str, int]:
        """Fetch raw XML data response from Crossref.

        Args:
            username (str): Crossref username.
            password (str): Crossref password.
            doi_prefix (str): DOI prefix associated with Crossref account.
            start_date (str): Date to start searching from, as YYYY-MM-DD.
            end_date (str): Date to search until, as YYYY-MM-DD
            api_url (str): Crossref cited-by API endpoint

        Returns:
            tuple: string response and int status code.
        """
        params = {
            'usr': username,
            'pwd': password,
            'doi': doi_prefix,
            'startDate': start_date,
            'endDate': end_date,
        }

        response = self.request_citation(params)
        if response.status_code != 200:
            sys.stderr.write(
                f'Could not retrieve cited-by citations ({response.reason})'
                f' - Request parameters: {params}); url: {api_url}'
            )

        return response.text, response.status_code

    def request_citation(self, params: dict) -> Response:
        """GET call to the Crossref cited-by API.

        Args:
            params (dict): usr, pwd, startDate, endDate.

        Returns:
            Response: Response from the Crossref service
        """
        return requests.get(self.cited_by_endpoint, params=params)

    @staticmethod
    def get_crossref_citations(xml_content: str) -> defaultdict[list]:
        """Extract raw data from Crossref citation XML for correct DOIs only.

        Args:
            xml_content (str): XML data returned from Crossref.

        Returns:
            dict: Each DOI that is cited and the citation entries for that DOI.
        """
        xml_data = BeautifulSoup(xml_content, features="xml")
        citations = defaultdict(list)
        for entry in xml_data.find_all('forward_link'):
            doi = entry.attrs.get('doi')
            citations[doi].extend(entry.find_all('journal_cite'))
            citations[doi].extend(entry.find_all('book_cite'))

        if None in citations:  # Remove entries with no DOI (if even possible).
            del citations[None]

        return citations

    def get_prime_doi(self, aliased_doi: str) -> str:
        """For aliased DOIs, determine the new DOI.

        Args:
            aliased_doi (str): Aliased DOI value.

        Returns:
            str: Resolved DOI value that the aliased DOI points to.
        """
        response = requests.get(
            'https://doi.crossref.org/servlet/query',
            params=dict(
                pid=self.tech_email,
                format='unixsd',
                id=aliased_doi
            )
        )
        xml_content = response.content
        xml_data = BeautifulSoup(xml_content, features="xml")

        items = xml_data.find_all('crm-item')
        for item in items:
            if item.attrs.get('name') == 'prime-doi':
                return item.text

        return ''

    def query_crossref_doi(self, doi: str) -> Response:
        """Make a request to crossref works endpoint to get info about a DOI.

        Args:
            doi (str): DOI of the work.

        Returns:
            Response: Unprocessed response received from the API.
        """
        return requests.get(
            f'https://api.crossref.org/v1/works/{doi}',
            params=dict(mailto=self.tech_email)
        )

    def get_doi_date_value(self, doi):
        response = self.query_crossref_doi(doi)

        if response.status_code == 404:
            prime_doi = self.get_prime_doi(doi)
            if not prime_doi:
                raise ValueError('Invalid DOI')

            response = self.query_crossref_doi(prime_doi)
            if response.status_code == 404:
                raise ValueError('Prime DOI not found')

        try:
            response_message = response.json()['message']
        except ValueError as e:
            logger.info(f'Error {e}')
            raise

        return self.fetch_publish_timestamp(response_message)

    @staticmethod
    def fetch_publish_timestamp(message: dict) -> str:
        """Get best guess for date published, based on the crossref response.

        Args:
            message: Message portion of the response from crossref.

        Returns:
            str: Publication timestamp in "YYYY-MM-DD HH:MM:SS" format.
        """
        keys = ['published', 'published-print', 'published-online', 'created']
        for key in keys:
            if key in message and len(message[key]['date-parts'][0]) == 3:
                year, month, day = message[key]['date-parts'][0]
                month, day = str(month).zfill(2), str(day).zfill(2)
                return f'{year}-{month}-{day} 00:00:00'

        raise ValueError('No valid publish date found')

    def get_citation_data(
            self,
            citation_entry: bs4.element.Tag,
    ) -> Citation(str, str):
        """Get citation data from parsed Crossref XML.

        Args:
            citation_entry (bs4.element.Tag): Citation from querying Crossref.

        Returns:
            Citation: containing cited-by DOI and timestamp.
        """
        cited_by_doi = citation_entry.find('doi').text
        timestamp = self.get_doi_date_value(cited_by_doi)

        return Citation(cited_by=cited_by_doi, timestamp=timestamp)


_TEMP_CLIENT = CrossrefCitedByClient(tech_email='support@crossref.org')


def fetch_citation_xml(*args, **kwargs):
    return _TEMP_CLIENT.fetch_citation_xml(*args, **kwargs)


def get_crossref_citations(*args, **kwargs):
    return _TEMP_CLIENT.get_citation_data(*args, **kwargs)


def get_citation_data(*args, **kwargs):
    return _TEMP_CLIENT.get_citation_data(*args, **kwargs)
