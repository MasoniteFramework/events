from masonite.app import App
from events import Event
import time

class UserAddedEvent:
    pass

class EventListener:

    def handle(self):
        pass

class TestEvent:

    def setup_method(self):
        self.app = App()
        self.app.bind('Event', Event(self.app))
    
    def test_add_listener(self):
        events = self.app.make('Event').listen(UserAddedEvent, [
            EventListener
        ])

        assert events.listeners == {UserAddedEvent: [EventListener]}

        events.listen(UserAddedEvent, [EventListener])

        assert events.listeners == {UserAddedEvent: [EventListener, EventListener]}
    
    def test_fire_event(self):
        events = self.app.make('Event').listen(UserAddedEvent, [
            EventListener
        ])

        assert events.fire(UserAddedEvent) is None
    
    def test_fire_event_with_string(self):
        listeners = []
        for i in range(1, 500):
            listeners.append(EventListener)

        event = self.app.make('Event').listen('user.registered', listeners)

        assert event.fire('user.registered') is None

