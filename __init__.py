from homeassistant.components.websocket_api import websocket_command
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

import asyncio
import websockets
import json

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    phone_number = entry.data["phone_number"]
    allowed_numbers_str = entry.data.get("allowed_phone_numbers", "")
    allowed_numbers = [num.strip() for num in allowed_numbers_str.splitlines() if num.strip()]
    special_messages_str = entry.data.get("special_messages", "")
    special_messages = [msg for msg in special_messages_str.splitlines() if msg.strip()]

    async def handle_websocket_message(websocket):
        async for message in websocket:
            message_data = json.loads(message)

            if "dataMessage" in message_data["envelope"]:
                source_number = message_data["envelope"]["source"]

                # Check if the source number is in the allowed list (or if the list is empty)
                if not allowed_numbers or source_number in allowed_numbers:
                    hass.bus.async_fire("signal_message_received", {"message": message_data})

    async def connect_to_websocket():
        url = f"ws://homeassistant.local:8888/v1/receive/{phone_number}"
        async with websockets.connect(url) as websocket:
            await handle_websocket_message(websocket)

    hass.loop.create_task(connect_to_websocket())
    return True

