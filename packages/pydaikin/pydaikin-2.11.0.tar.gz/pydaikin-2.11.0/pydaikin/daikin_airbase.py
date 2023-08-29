"""Pydaikin appliance, represent a Daikin AirBase device."""

import logging
from urllib.parse import quote, unquote

from .daikin_brp069 import DaikinBRP069

_LOGGER = logging.getLogger(__name__)


class DaikinAirBase(DaikinBRP069):
    """Daikin class for AirBase (BRP15B61) units."""

    TRANSLATIONS = dict(
        DaikinBRP069.TRANSLATIONS,
        **{
            "mode": {
                "0": "fan",
                "1": "hot",
                "2": "cool",
                "3": "auto",
                "7": "dry",
            },
            "f_rate": {
                "0": "auto",
                "1": "low",
                "3": "mid",
                "5": "high",
                "1a": "low/auto",
                "3a": "mid/auto",
                "5a": "high/auto",
            },
        },
    )

    HTTP_RESOURCES = [
        "common/basic_info",
        "aircon/get_control_info",
        "aircon/get_model_info",
        "aircon/get_sensor_info",
        "aircon/get_zone_setting",
    ]

    INFO_RESOURCES = DaikinBRP069.INFO_RESOURCES + ["aircon/get_zone_setting"]

    DEFAULTS = {"htemp": "-", "otemp": "-", "shum": "--"}

    @staticmethod
    def parse_response(response_body):
        """Parse response from Daikin, add support for f_rate-auto."""
        _LOGGER.debug("Parsing %s", response_body)
        response = super(DaikinAirBase, DaikinAirBase).parse_response(response_body)
        if response.get("f_auto") == "1":
            response["f_rate"] = f'{response["f_rate"]}a'

        # Translate swing mode from 2 parameters to 1
        if response.get("f_dir_ud") == "0" and response.get("f_dir_lr") == "0":
            response["f_dir"] = '0'
        if response.get("f_dir_ud") == "S" and response.get("f_dir_lr") == "0":
            response["f_dir"] = '1'
        if response.get("f_dir_ud") == "0" and response.get("f_dir_lr") == "S":
            response["f_dir"] = '2'
        if response.get("f_dir_ud") == "S" and response.get("f_dir_lr") == "S":
            response["f_dir"] = '3'

        return response

    def __init__(
        self, device_id, session=None
    ):  # pylint:disable=useless-super-delegation
        """Init the pydaikin appliance, representing one Daikin AirBase
        (BRP15B61) device."""
        super().__init__(device_id, session)

    async def init(self):
        """Init status and set defaults."""
        await super().init()
        if not self.values:
            raise Exception("Empty values.")
        self.values.update({**self.DEFAULTS, **self.values})

    async def _run_get_resource(self, resource):
        """Make the http request."""
        resource = "skyfi/%s" % resource
        return await super()._run_get_resource(resource)

    @property
    def support_away_mode(self):
        """Return True if the device support away_mode."""
        return False

    @property
    def support_swing_mode(self):
        """Return True if the device support setting swing_mode."""
        return 'f_dir_ud' in self.values and 'f_dir_lr' in self.values

    @property
    def support_outside_temperature(self):
        """AirBase unit returns otemp if master controller starts before it."""
        return True

    @property
    def support_zone_temperature(self):
        """Return True if the device support setting zone_temperature."""
        return "lztemp_h" in self.values

    @property
    def fan_rate(self):
        """Return list of supported fan rates."""
        fan_rates = list(map(str.title, self.TRANSLATIONS.get("f_rate", {}).values()))
        if self.values.get("frate_steps") == "2":
            if self.values.get("en_frate_auto") == "0":
                return fan_rates[1:4:2]
            return fan_rates[:3:2] + fan_rates[3::2]
        if self.values.get("en_frate_auto") == "0":
            return fan_rates[1:4]
        return fan_rates

    async def _update_settings(self, settings):
        """Update settings to set on Daikin device."""

        # Call the base BRP069 method to update the settings; it will
        # return the current values it retrieves from the controller
        # so we can further process them
        current_val = await super()._update_settings(settings)

        # f_auto requires some special handling, as it is managed as an
        # attribute of f_rate and we don't directly set it - so when f_rate
        # is being changed, ensure we update f_auto accordingly if it is
        # defined in the current device's returned settings
        if "f_auto" in current_val:
            # The system supports f_auto; if we are setting the fan speed
            # then ensure we update the f_auto setting as well
            if "f_rate" in settings:
                self.values["f_auto"] = "1" if "a" in self.values["f_rate"] else "0"
            else:
                key = "auto" + self.values["mode"]
                if key in current_val:
                    self.values["f_auto"] = current_val[key]

                    # The f_rate value would have been retrieved from the unit's current
                    # operating mode fan rate setting, and needs the 'a' suffix reinstated
                    # if we are running in an automatic fan speed mode
                    if self.values["f_auto"] == "1":
                        self.values["f_rate"] = f'{self.values["f_rate"]}a'

        return current_val

    async def set(self, settings):
        """Set settings on Daikin device."""
        await self._update_settings(settings)

        self.values.setdefault("f_airside", 0)
        query_c = (
            "aircon/set_control_info"
            "?pow={pow}&mode={mode}&stemp={stemp}&shum={shum}"
            "&f_rate={f_rate[0]}&f_auto={f_auto}&f_dir={f_dir}"
            "&lpw=&f_airside={f_airside}"
        ).format(**self.values)

        # Australian version uses 2 separate parameters instead of the combined f_dir
        if self.support_swing_mode:
            f_dir_ud = 'S' if self.values['f_dir'] in ('1', '3') else '0'
            f_dir_lr = 'S' if self.values['f_dir'] in ('2', '3') else '0'
            query_c += '&f_dir_ud=%s&f_dir_lr=%s' % (f_dir_ud, f_dir_lr)

        _LOGGER.debug("Sending query_c: %s", query_c)
        await self._get_resource(query_c)

    def represent(self, key):
        """Return translated value from key."""
        k, val = super().represent(key)

        if key in ["zone_name", "zone_onoff", "lztemp_h"]:
            val = unquote(self.values[key]).split(";")

        return (k, val)

    @property
    def zones(self):
        """Return list of zones."""
        if not self.values.get("zone_name"):
            return None
        zone_onoff = self.represent("zone_onoff")[1]
        if self.support_zone_temperature:
            zone_temp = self.represent("lztemp_h")[1]
            return [
                (name.strip(" +,"), zone_onoff[i], float(zone_temp[i]))
                for i, name in enumerate(self.represent("zone_name")[1])
            ]
        return [
            (name.strip(" +,"), zone_onoff[i], 0)
            for i, name in enumerate(self.represent("zone_name")[1])
        ]

    async def set_zone(self, zone_id, key, value):
        """Set zone status."""
        current_state = await self._get_resource("aircon/get_zone_setting")
        self.values.update(current_state)
        current_group = self.represent(key)[1]
        current_group[zone_id] = value
        self.values[key] = quote(";".join(current_group)).lower()

        query = "aircon/set_zone_setting?zone_name={}&zone_onoff={}".format(
            current_state["zone_name"],
            self.values["zone_onoff"],
        )

        if self.support_zone_temperature:
            query += "&lztemp_h=%s" % self.values["lztemp_h"]

        _LOGGER.debug("Set zone:: %s", query)
        await self._get_resource(query)
