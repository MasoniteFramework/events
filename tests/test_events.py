from masonite.app import App
from events import Event
import time
import pytest
from events.exceptions import InvalidSubscriptionType

class UserAddedEvent:
    pass

class EventListener:

    def handle(self):
        pass

class EventWithSubscriber:

    subscribe = ['user.registered']

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

    def test_event_subscribers(self):
        self.app.make('Event').listeners = {}
        events = self.app.make('Event').subscribe(EventWithSubscriber)

        assert self.app.make('Event').listeners == {'user.registered': [EventWithSubscriber]}

    def test_event_with_multiple_subscribers(self):
        self.app.make('Event').listeners = {}
        event = EventWithSubscriber

        event.subscribe = ['user.registered', 'user.subscribed']

        events = self.app.make('Event').subscribe(event)

        assert self.app.make('Event').listeners == {'user.registered': [EventWithSubscriber], 'user.subscribed': [EventWithSubscriber]}
    
    def test_event_with_throws_exception_with_invalid_subscribe_attribute_type(self):
        self.app.make('Event').listeners = {}
        event = EventWithSubscriber

        event.subscribe = 'user.registered'

        with pytest.raises(InvalidSubscriptionType):
            self.app.make('Event').subscribe(event)

    def test_event_starts_event_observer(self):
        self.app.make('Event').listeners = {}
        self.app.make('Event').event('user.subscribed')
        assert self.app.make('Event').listeners == {'user.subscribed': []}
