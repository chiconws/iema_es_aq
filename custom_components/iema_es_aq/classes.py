"""IEMA Espírito Santo Qualidade do Ar - Classes."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
)

from .const import POLLUTANT_TYPE


class IemaBaseDescription(SensorEntityDescription):
    """Base sensor entity description."""

    native_unit_of_measurement = CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    state_class = SensorStateClass.MEASUREMENT
    icon = 'mdi:chart-bar'

class CarbonMonoxideDescription(IemaBaseDescription):
    """Carbon monoxide sensor entity description."""

    key: POLLUTANT_TYPE = 'Monóxido de Carbono'
    device_class = SensorDeviceClass.CO
    native_unit_of_measurement = CONCENTRATION_PARTS_PER_MILLION
    translation_key = 'carbon_monoxide'
    icon = 'mdi:molecule-co'

class NitrogenDioxideDescription(IemaBaseDescription):
    """Notrogen dioxide sensor entity description."""

    key = 'Dióxido de Nitrogênio'
    device_class = SensorDeviceClass.NITROGEN_DIOXIDE
    translation_key = 'nitrogen_dioxide'

class OzoneDescription(IemaBaseDescription):
    """Ozone sensor entity description."""

    key = 'Ozônio'
    device_class = SensorDeviceClass.OZONE
    translation_key = 'ozone'

class SulphurDioxideDescription(IemaBaseDescription):
    """Sulphur dioxide sensor entity description."""

    key = 'Dióxido de Enxofre'
    device_class = SensorDeviceClass.SULPHUR_DIOXIDE
    translation_key = 'sulphur_dioxide'

class PM25Description(IemaBaseDescription):
    """PM25 sensor entity description."""

    key = 'Partículas Respiráveis (<2,5µm)'
    device_class = SensorDeviceClass.PM25
    translation_key = 'pm25'

class PM10Description(IemaBaseDescription):
    """PM10 sensor entity description."""

    key = 'Partículas Respiráveis (<10µm)'
    device_class = SensorDeviceClass.PM10
    translation_key = 'pm10'
