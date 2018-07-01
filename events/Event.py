class Event:
    listeners = {}
    _fired_events = {}

    def __init__(self, container):
        self.container = container

    def listen(self, event, listeners = []):
        if event in self.listeners:
            self.listeners[event] += listeners
            return self
        
        self.listeners.update({event: listeners})
        return self
    
    # TODO: Add wildcard like self.fire('user.*')
    def fire(self, events):
        fired_listeners = {}
        if isinstance(events, str) and '*' in events:
            for event_action, listener_events in self.listeners.items():
                fired_listeners.update({event_action: []})
                for listener in listener_events:
                    search = events.split('*')
                    if events.endswith('*') and event_action.startswith(search[0]) \
                    or events.startswith('*') and event_action.endswith(search[1]) \
                    or event_action.startswith(search[0]) and event_action.endswith(search[1]):
                        fired_listeners[event_action].append(listener)
                        event = self.container.resolve(listener)
                        self.container.resolve(event.handle)       
        else:
            for event in self.listeners[events]:
                event = self.container.resolve(event)
                self.container.resolve(event.handle)

        self._fired_events = self.clear_blank_fired_events(fired_listeners)
    
    def clear_blank_fired_events(self, fired_listeners):
        new_dictionary = {}
        for event, listeners in fired_listeners.items():
            if listeners:
                new_dictionary.update({event: listeners})

        return new_dictionary