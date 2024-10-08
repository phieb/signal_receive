import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.data_entry_flow import section

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
                errors["phone_number"] = "You're sender number has invalid syntax. Please start with +. eg +4998765432"

            # Handle allowed phone numbers as a comma-separated string
            allowed_numbers_str = user_input["allowed_phone_numbers"]

            # Validate the allowed phone numbers (optional)
            if allowed_numbers_str:
                for number in allowed_numbers_str.splitlines():
                    if not number.strip().startswith("+"):
                        errors["allowed_phone_numbers"] = f"Invalid number: {number.strip()}"
                        break

            # Validate any special messages
            special_messages_str = user_input["special_messages"]

            if special_messages_str:
                for msg in special_messages_str.splitlines():
                    if len(msg) > 50: 
                        errors["special_messages"] = f"message exceeds 50 chars: {msg}"  
                        break
            if not errors:
                return self.async_create_entry(title="Signal Receive", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("phone_number"): str,
                vol.Optional("allowed_phone_numbers", default=""): str,
                "messages": section(
                    vol.Schema({
                        vol.Optional("special_messages", default=""): str,
                    })
                )
            }),
            errors=errors,
            description_placeholders={
                "phone_number":"With Signal Plugin registered phone number which will receive the messages e.g. +44123456789",
                "allowed_phone_numbers":"If not empty the integration will only create events, if the sender is in this list (one number per line)",
                "special_messages":"the integration will generate an event for each special message (one message per line - max 50 chars)"
            },
        )

