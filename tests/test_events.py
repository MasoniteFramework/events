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
        event = Event(self.app)

        self.app.bind('Event', event)
    def test_fire_event_with_wildcard_ends_with(self):
        events = self.app.make('Event').listen('user.registered', [
            EventListener, EventListener
        ])

        events = self.app.make('Event').listen('user.subscribed', [
            EventListener
        ])

        event = self.app.make('Event')

        assert event.fire('*.registered') is None
        assert event._fired_events == {'user.registered': [EventListener, EventListener]}

    def test_add_listener(self):
        self.app.make('Event').listeners = {}
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

    def test_fire_event_with_wildcard_starts_with(self):
        self.app.make('Event').listeners = {}
        events = self.app.make('Event').listen('user.registered', [
            EventListener
        ])
        events = self.app.make('Event').listen('user.subscribed', [
            EventListener
        ])

        event = self.app.make('Event')

        assert event.fire('user.*') is None
        assert event._fired_events == {'user.registered': [EventListener], 'user.subscribed': [EventListener]}

    def test_fire_event_with_wildcard_in_middle_of_fired_event(self):
        self.app.make('Event').listeners = {}
        events = self.app.make('Event').listen('user.manager.registered', [
            EventListener
        ])
        events = self.app.make('Event').listen('user.owner.subscribed', [
            EventListener
        ])

        event = self.app.make('Event')

        assert event.fire('user.*.registered') is None
        assert event._fired_events == {'user.manager.registered': [EventListener]}

