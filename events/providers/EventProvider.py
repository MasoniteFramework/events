""" An EventProvider Service Provider """

import builtins

from masonite.provider import ServiceProvider

from events import Event
from events.commands import EventCommand


class EventProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('Event', Event(self.app))
        self.app.bind('EventCommand', EventCommand())
        builtins.event = self.app.make('Event').fire

    def boot(self):
        pass
