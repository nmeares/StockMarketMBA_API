import StockMarketMBA.lib as lib
from requests.sessions import session
from configparser import ConfigParser
import json

HEADERS_PATH = './headers.json'
urls = ConfigParser()['URLS']


class api():

    def __init__(self):
        # Initiate
        self.s = session()
        with open(HEADERS_PATH) as f:
            self.HEADERS = json.load(f)
        self.symbols_url = urls['SYMBOL_LOOKUP']
        self.on_exch_url = urls['SECS_ON_EXCHANGE']
        self.exch_symbols_url = urls['EXCHANGE_SYMBOLS']
        self.spacs_url = urls['PENDING_SPACS']

    def symbol_lookup(self, ticker:str) -> dict:
        '''Look up the security identifiers for a specified ticker.
        

        Parameters
        ----------
        ticker : str
            ticker symbol

        Returns
        -------
        dict
            returns a JSON response object
        '''
        url = self.symbols_url
        # Retrieve version ID from web form
        forms = lib.get_forms(url, self.s)[1]
        details = lib.form_details(forms)
        version = lib.get_version(details)

        # Add ticker and version ID to search payload
        payload = 'action=Go&search={}&version={}'.format(ticker, version)

        # Request and find table
        r = self.s.post(url, headers=self.HEADERS, data=payload)
        return lib.get_table(r.text, 'searchtable')

    def exch_secs(self, exchange_code:str) -> dict:
        '''Lookup all stocks listed on a sepcified exchange.

        Parameters
        ----------
        exchange_code : str
            [description]

        Returns
        -------
        dict
            [description]
        '''
        url = self.on_exch_url
        payload = 'action=Go&exchangecode={}'.format(exchange_code)

        # Request and find table
        r = self.s.post(url, headers=self.HEADERS, data=payload)
        return lib.get_table(r.text, 'ETFs')

    def exch_symbols(self) -> dict:
        url = self.exch_symbols_url

        r = self.s.get(url)
        return lib.get_table(r.text, 'ETFs')

    def pending_SPACs(self) -> dict:
        url = self.spacs_url

        r = self.s.get(url)
        return lib.get_table(r.text, 'ETFs')
