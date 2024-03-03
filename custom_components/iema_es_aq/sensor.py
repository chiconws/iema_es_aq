"""IEMA Espírito Santo Qualidade do Ar - Sensors."""
from datetime import timedelta
from typing import Optional

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import IemaApi
from .classes import (
    CarbonMonoxideDescription,
    NitrogenDioxideDescription,
    OzoneDescription,
    PM10Description,
    PM25Description,
    SulphurDioxideDescription,
)
from .const import CONF_STATION_ID, DOMAIN

NAME = DOMAIN
ISSUEURL = 'https://github.com/chiconws/iema_es_aq/issues'

STARTUP = f"""
-------------------------------------------------------------------
{NAME}
This is a custom component
If you have any issues with this you need to open an issue here:
{ISSUEURL}
-------------------------------------------------------------------
"""

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_STATION_ID): cv.string
})

UPDATE_INTERVAL = timedelta(minutes=30)

async def async_setup_platform(
        hass: HomeAssistant,
        config: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
        discovery_info=None
    ):
    """Async Setup Platform."""
    station_id = config.get(CONF_STATION_ID)

    api = IemaApi(station_id)

    sensors = []
    sensors.append(IemaCarbonMonoxideSensor(api))
    sensors.append(IemaNitrogenDioxideSensor(api))
    sensors.append(IemaSulphurDioxideSensor(api))
    sensors.append(IemaOzoneSensor(api))
    sensors.append(IemaPM25Sensor(api))
    sensors.append(IemaPM10Sensor(api))
    async_add_entities(sensors, True)


class IemaBaseSensor(Entity):
    """IEMA Sensor Base."""

    entity_description: SensorEntityDescription
    state: Optional[float] = None
    state_attributes = {}
    api: IemaApi

    @property
    def name(self):
        """Name."""
        return f'{self.entity_description.key}'

    @property
    def unique_id(self):
        """Unique ID."""
        return f'{DOMAIN}_{self.name}_{self.api.station_id}'

    @property
    def native_unit_of_measurement(self):
        """Native Unit of Measurement."""
        return self.entity_description.native_unit_of_measurement

    @property
    def state_class(self):
        """State Class."""
        return self.entity_description.state_class

    @property
    def icon(self):
        """Icon."""
        return self.entity_description.icon

    def update(self) -> None:
        """Update method."""
        try:
            response = self.api.get_data()[self.name]
        except KeyError:
            self.state = None
            return

        self.state = response['ValorIqa']
        self.state_attributes['acronym'] = response['PoluenteSigla']
        self.state_attributes['quality'] = response['FaixaIQA']
        self.state_attributes['last updated'] = response['DataHora']
        self.state_attributes['location'] = response['Localizacao']
        self.state_attributes['latitude'] = response['Latitude']
        self.state_attributes['longitude'] = response['Longitude']

class IemaCarbonMonoxideSensor(IemaBaseSensor):
    """Carbon Monoxide Sensor Class."""

    def __init__(self, api: IemaApi) -> None:
        """Init."""
        self.entity_description = CarbonMonoxideDescription
        self.api = api

class IemaNitrogenDioxideSensor(IemaBaseSensor):
    """Nitrogen Dioxide Sensor Class."""

    def __init__(self, api: IemaApi) -> None:
        """Init."""
        self.entity_description = NitrogenDioxideDescription
        self.api = api

class IemaOzoneSensor(IemaBaseSensor):
    """Ozone Sensor Class."""

    def __init__(self, api: IemaApi) -> None:
        """Init."""
        self.entity_description = OzoneDescription
        self.api = api

class IemaSulphurDioxideSensor(IemaBaseSensor):
    """Sulphur Dioxide Sensor Class."""

    def __init__(self, api: IemaApi) -> None:
        """Init."""
        self.entity_description = SulphurDioxideDescription
        self.api = api

class IemaPM25Sensor(IemaBaseSensor):
    """PM25 Sensor Class."""

    def __init__(self, api: IemaApi) -> None:
        """Init."""
        self.entity_description = PM25Description
        self.api = api

class IemaPM10Sensor(IemaBaseSensor):
    """PM10 Sensor Class."""

    def __init__(self, api: IemaApi) -> None:
        """Init."""
        self.entity_description = PM10Description
        self.api = api
