from pathlib import Path

import pytest
import responses

from fixer_currency import FixerClient
from fixer_currency.exceptions import FixerException

BASE_URL = "https://api.apilayer.com/fixer/"
RESPONSES_DIR = Path(__file__).parent / "responses"


class TestAvailableCurrencies:
    @classmethod
    def setup_class(cls):
        cls.access_key = "test-access-key"
        cls.url = BASE_URL + "symbols"
        cls.response_file = RESPONSES_DIR / "available_currencies_responses.yaml"

    @responses.activate
    def test_returns_available_currencies(self):
        responses._add_from_file(self.response_file)
        client = FixerClient(self.access_key)
        response = client.available_currencies()

        assert response["success"] is True
        assert response["symbols"]["AED"] == "United Arab Emirates Dirham"
        assert response["symbols"]["CRC"] == "Costa Rican Colón"

    @responses.activate
    def test_raises_exception_if_bad_request(self):
        responses.add(
            responses.GET,
            self.url,
            body="{'success': false}",
            status=400,
            content_type="application/json",
        )

        with pytest.raises(FixerException):
            client = FixerClient(self.access_key)
            client.available_currencies()
