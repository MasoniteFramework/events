class Event:
    listeners = {}

    def __init__(self, container):
        self.container = container

    def listen(self, event, listeners = []):
        if event in self.listeners:
            self.listeners[event] += listeners
            return self
        
        self.listeners.update({event: listeners})
        return self
    
    def fire(self, events):
        for event in self.listeners[events]:
            event = self.container.resolve(event)
            self.container.resolve(event.handle)
