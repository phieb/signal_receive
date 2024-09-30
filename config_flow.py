import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN  # Assuming you have a const.py file with DOMAIN defined

class SignalReceiveConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Signal Receive."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the phone number (you can add more complex validation here)
            if not user_input["phone_number"].startswith("+"):
                errors["base"] = "invalid_phone_number"
            else:
                return self.async_create_entry(title="Signal Receive", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("phone_number"): str,
            }),
            errors=errors,
        )

