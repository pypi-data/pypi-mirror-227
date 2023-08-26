import datetime
from typing import Dict, Iterable, Optional, Union
from urllib.parse import urlencode

import requests

from fixer_currency.exceptions import FixerException

BASE_URL = "https://api.apilayer.com/fixer/"
API_TIMEOUT = 15


class FixerClient:
    """A client for Fixer API, available on API Layer."""

    def __init__(
        self,
        access_key: str,
        base: str = "EUR",
        symbols: Union[None, str, Iterable[str]] = None,
    ):
        """Create FixerClient object.

        :param access_key: your API Key.
        :param base: base symbol (default is "EUR")
        :param symbols: currency symbol(s) to always request specific exchange rates.
        """
        self._access_key = access_key
        self._base = base
        self._symbols = symbols

    def _create_headers(self) -> Dict[str, str]:
        """Creates a header with the API key required for accessing Fixer API
        on API Layer.
        """
        headers = {"apikey": self._access_key}
        return headers

    def _create_payload(self, symbols: Union[None, str, Iterable[str]]) -> str:
        """Creates a payload with no empty values.

        :param symbols: currency symbol(s) to request specific exchange rates.
        :return: a payload.
        """
        payload = {}
        payload["base"] = self._base
        if symbols is not None:
            if isinstance(symbols, str):
                payload["symbols"] = symbols
            else:
                payload["symbols"] = ",".join(symbols)

        payload_str = urlencode(payload, safe=",")
        return payload_str

    def available_currencies(self) -> dict:
        """Get all currency symbols that can be used as base or target.

        :return: a dictinary where the member `symbols` contains a mapping
            from currency symbols to the full currency name.
        :raises FixerException: if any error making a request.
        """
        try:
            url = BASE_URL + "symbols"
            response = requests.get(url, headers=self._create_headers(), timeout=API_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            raise FixerException(str(exc)) from exc

    def latest(self, symbols: Union[None, str, Iterable[str]] = None) -> dict:
        """Get the latest foreign exchange reference rates.

        :param symbols: currency symbol(s) to request specific exchange rates.
        :return: the latest foreign exchange reference rates.
        :raises FixerException: if any error making a request.
        """
        try:
            headers = self._create_headers()
            symbols = symbols or self._symbols
            payload = self._create_payload(symbols)

            url = BASE_URL + "latest"

            response = requests.get(url, headers=headers, params=payload, timeout=API_TIMEOUT)

            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as exc:
            raise FixerException(str(exc)) from exc

    def historical_rates(
        self, date: Union[datetime.date, str], symbols: Optional[Union[str, Iterable[str]]] = None
    ) -> dict:
        """Get rates for a historical date.

        :param date: the date to get rates for.
        :param symbols: currency symbol(s) to request specific exchange rates.
        :return: the historical rates for a specific date.
        :raises FixerException: if any error making a request.
        """
        try:
            if isinstance(date, datetime.date):
                # Convert date to ISO 8601 format.
                date = date.isoformat()

            symbols = symbols or self._symbols
            headers = self._create_headers()
            payload = self._create_payload(symbols)

            url = BASE_URL + date

            response = requests.get(url, headers=headers, params=payload, timeout=API_TIMEOUT)

            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as exc:
            raise FixerException(str(exc)) from exc
