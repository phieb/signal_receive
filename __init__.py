from homeassistant.components.websocket_api import websocket_command
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

import asyncio
import websockets

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.warning("Setting up Signal Receive integration")  # Log when the integration starts
    phone_number = entry.data["phone_number"]
    _LOGGER.debug("Using phone number: %s", phone_number)  # Log the configured phone number

    async def handle_websocket_message(websocket):
        async for message in websocket:
            _LOGGER.warning("Received message: %s", message)  # Log received messages
            hass.bus.async_fire("signal_message_received", {"message": message})

    async def connect_to_websocket():
        url = f"ws://homeassistant.local:8888/v1/receive/{phone_number}"
        _LOGGER.warning("Connecting to websocket with url: %s", url)  # Log received messages
        async with websockets.connect(url) as websocket:
            await handle_websocket_message(websocket)

    hass.loop.create_task(connect_to_websocket())
    return True

