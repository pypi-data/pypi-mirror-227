from typing import Callable, Union, Any, Dict, Set


class EventEmitter():
    """
    A simple event emitter for subscribing to topics and emitting events.
    """

    def __init__(self) -> None:
        self.subscriptions: Dict[str, Set[Callable]] = {}

    def subscribe(self, topic: str, callback: Callable):
        """
        Subscribe to a topic with a callback.

        Args:
            topic (str): The topic to subscribe to.
            callback (Callable): The function to be called when the topic is emitted.

        Returns:
            Subscription: An object representing the subscription which can be used to unsubscribe.
        """
        self._validate_topic(topic)
        self._validate_callback(callback)
        handlers = self.subscriptions.get(topic, set())
        handlers.add(callback)
        self.subscriptions[topic] = handlers
        return Subscription(topic, callback, handlers)

    def emit(self, topic: str, data: Union[Any, None]):
        """
        Emit an event for a given topic with optional data.

        Args:
            topic (str): The topic to emit.
            data (Union[Any, None]): The data to pass to subscribed callbacks. Default is None.

        Raises:
            EventEmitterException: If the topic does not exists.
        """
        self._validate_topic(topic)
        if not (topic in self.subscriptions):
            raise EventEmitterException("There is not such a topic")
        for callable in self.subscriptions.get(topic).copy():
            try:
                callable(topic, data)
            except:
                pass

    def _validate_topic(self, topic: str):
        if not topic:
            raise EventEmitterException("Topic is required")

    def _validate_callback(self, callback: Callable):
        if not callback:
            raise EventEmitterException("Callable is required")


class EventEmitterException(Exception):
    def __init__(self, message: str = "EventEmitter error"):
        super().__init__(message)

    def __str__(self):
        original_message = super().__str__()
        return f"EventEmitter error: {original_message}"


class Subscription():
    def __init__(self, topic: str, callback: Callable, handlers: Set[Callable]):
        self.handlers: Set = handlers
        self.callback: Callable = callback
        self.topic: str = topic

    def unsubscribe(self):
        """
        Remove the callback from the handlers.

        Raises:
            EventEmitterException: If the callback is not found in the handlers for the topic.
        """
        if self.callback in self.handlers:
            self.handlers.remove(self.callback)
        else:
            raise EventEmitterException(
                f"There is not callback subscribed to topic={self.topic}")


class GlobalEventEmitter(EventEmitter):
    __instance: Union[EventEmitter, None] = None

    def __new__(cls, *args, **kwargs) -> Any:
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            # Ensure the parent's __init__ is called only once
            super(GlobalEventEmitter, cls.__instance).__init__()
        return cls.__instance

    def __init__(self) -> None:
        pass  # The base class initialization is done in the __new__ method
