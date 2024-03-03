"""IEMA Espírito Santo Qualidade do Ar - API."""
from datetime import datetime

import requests

from .const import BASE_URL


class IemaApi:
    """API."""

    def __init__(self, station_id) -> None:
        """Init."""
        self.station_id = int(station_id)
        self._url = f'{BASE_URL}/{station_id}'

    def get_data(self) -> dict:
        """Return data."""

        response = requests.get(self._url, timeout=50)
        root_response = requests.get(BASE_URL, timeout=50)

        if not response.ok or not root_response.ok:
            return

        sensors_data = response.json()
        root_data = root_response.json()
        for item in root_data:
            if item['IdEstacao'] == self.station_id:
                station_data = item
                break

        return self._parse_data(sensors_data, station_data)

    def _parse_data(
            self,
            sensors_data: list[dict],
            station_data: list[dict]
    ) -> list[dict]:
        """Parse data."""

        for d in sensors_data:
            d['DataHora'] = datetime.fromisoformat(d['DataHora'][-1])
            d['ValorIqa'] = float(d['ValorIqa'][-1])
            d['FaixaIQA'] = d['FaixaIQA'][-1]
            del d['Max'], d['Min'], d['Cor']

        sensors_data = {
            item['Poluente']: {
                key: value
                for key, value in item.items()
                if key != 'Poluente'
                if key != 'Estacao'
            }
            for item in sensors_data
        }

        for item in sensors_data:
            sensors_data[item]['Localizacao'] = station_data['Localizacao']
            sensors_data[item]['Latitude'] = station_data['Latitude']
            sensors_data[item]['Longitude'] = station_data['Longitude']

        return sensors_data
