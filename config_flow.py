import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

class SignalReceiveConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Signal Receive."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the phone number
            if not user_input["phone_number"].startswith("+"):
                errors["base"] = "invalid_phone_number"

            # Handle allowed phone numbers as a comma-separated string
            allowed_numbers_str = user_input.get("allowed_phone_numbers", "")

            # Validate the allowed phone numbers (optional)
            if allowed_numbers_str:
                for number in allowed_numbers_str.split(","):
                    if not number.strip().startswith("+"):
                        errors["base"] = "invalid_allowed_numbers"
                        break

            if not errors:
                return self.async_create_entry(title="Signal Receive", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("phone_number"): str,
                vol.Optional("allowed_phone_numbers", default=""): str,  # Use a string for input
            }),
            errors=errors,
        )

