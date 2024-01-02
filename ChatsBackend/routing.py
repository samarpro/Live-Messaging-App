from django.urls import path
from .consumers import ChatHandlerConsumer


websocket_patterns = [
    path('<str:receiver_name>/',ChatHandlerConsumer.as_asgi()) # Please add necessary name
]