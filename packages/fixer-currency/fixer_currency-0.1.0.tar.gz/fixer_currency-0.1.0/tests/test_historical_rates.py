from datetime import date
from pathlib import Path

import pytest
import responses

from fixer_currency import FixerClient
from fixer_currency.exceptions import FixerException

BASE_URL = "https://api.apilayer.com/fixer/"
RESPONSES_DIR = Path(__file__).parent / "responses"


class TestHistoricalRates:
    @classmethod
    def setup_class(cls):
        cls.access_key = "test-access-key"
        cls.date = date(2000, 1, 3)
        cls.path = f"{cls.date.isoformat()}"
        cls.url = BASE_URL + cls.path
        cls.response_file = RESPONSES_DIR / "historical_rates_responses.yaml"

    @responses.activate
    def test_returns_historical_eur_as_default_base(self):
        responses._add_from_file(file_path=self.response_file)
        client = FixerClient(self.access_key)

        response = client.historical_rates(self.date, symbols=["GBP"])

        assert response["success"] is True
        assert response["base"] == "EUR"

    @responses.activate
    def test_returns_historical_eur_to_gbp_rate(self):
        responses._add_from_file(file_path=self.response_file)

        client = FixerClient(self.access_key, base="EUR")
        for date_variant in [self.date, self.date.isoformat()]:
            response = client.historical_rates(date_variant, symbols=["GBP"])

            assert response["success"] is True
            assert response["base"] == "EUR"
            assert response["date"] == "2000-01-03"
            assert response["rates"]["GBP"] == 0.627016

            request = responses.calls[0].request
            assert request.method == "GET"
            assert request.headers["apikey"] == self.access_key
            assert request.body is None

    @responses.activate
    def test_returns_historical_usd_to_gbp_rate(self):
        responses._add_from_file(file_path=self.response_file)

        client = FixerClient(self.access_key, base="USD")
        response = client.historical_rates(self.date, symbols=["GBP"])

        assert response["success"] is True
        assert response["base"] == "USD"
        assert response["date"] == "2000-01-03"
        assert response["rates"]["GBP"] == 0.614647

    @responses.activate
    def test_returns_historical_rates_for_symbols_passed_in_constructor(self):
        responses._add_from_file(file_path=self.response_file)
        symbols = ["USD", "GBP"]

        client = FixerClient(self.access_key, symbols=symbols)
        response = client.historical_rates(self.date)

        assert response["success"] is True
        assert response["date"] == "2000-01-03"
        assert response["rates"]["GBP"] == 0.627016
        assert response["rates"]["USD"] == 1.020124

    @responses.activate
    def test_returns_historical_rates_for_symbols_passed_in_method(self):
        responses._add_from_file(file_path=self.response_file)
        symbols = ["USD", "GBP"]

        client = FixerClient(self.access_key)
        response = client.historical_rates(self.date, symbols=symbols)

        assert response["success"] is True
        assert response["date"] == "2000-01-03"
        assert response["rates"]["USD"] == 1.020124
        assert response["rates"]["GBP"] == 0.627016

    @responses.activate
    def test_returns_hist_rates_for_symbols_passed_in_method_if_both(self):
        responses._add_from_file(file_path=self.response_file)

        symbols = ["USD", "GBP"]
        other_symbols = ["JPY", "EUR"]

        client = FixerClient(self.access_key, symbols=other_symbols)
        response = client.historical_rates(date=self.date, symbols=symbols)

        assert response["rates"]["USD"] == 1.020124
        assert response["rates"]["GBP"] == 0.627016
        assert response["rates"].get("JPY") is None
        assert response["rates"].get("EUR") is None

    @responses.activate
    def test_raises_exception_if_bad_request(self):
        responses.add(
            responses.GET, self.url, body="{'success': false}", status=400, content_type="text/json"
        )
        with pytest.raises(FixerException):
            client = FixerClient(self.access_key)
            client.historical_rates(date=self.date)
