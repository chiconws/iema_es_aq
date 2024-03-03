"""IEMA Espírito Santo Qualidade do Ar - Constants."""

from typing import Literal

BASE_URL = 'https://qualidadedoarapi.es.gov.br/api/mapa'
DOMAIN = 'iema_es_aq'
SENSOR_NAME = 'IEMA - Espírito Santo - Qualidade do Ar'

CONF_STATION_ID = 'station_id'

POLLUTANT_TYPE = Literal[
    'Monóxido de Carbono',
    'Dióxido de Nitrogênio',
    'Ozônio',
    'Dióxido de Enxofre',
    'Partículas Respiráveis (<2,5µm)',
    'Partículas Respiráveis (<10µm)'
]
