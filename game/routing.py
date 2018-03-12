from channels import route

from . import consumers

channel_routing = [
    route('websocket.connect', consumers.ws_connect),
    route('websocket.recieve', consumers.ws_recieve),
    route('websocket.disconnect', consumers.ws_disconnect),
]

