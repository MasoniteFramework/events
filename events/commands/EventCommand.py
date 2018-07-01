""" A EventCommand Command """
from cleo import Command
import os


class EventCommand(Command):
    """
    Description of command

    event:listener
        {name : Name of the event you want to create}
    """

    def handle(self):
        event = self.argument('name')
        if not os.path.isfile('app/events/{0}.py'.format(event)):
            if not os.path.exists(os.path.dirname('app/events/{0}.py'.format(event))):
                # Create the path to the event if it does not exist
                os.makedirs(os.path.dirname('app/events/{0}.py'.format(event)))

            f = open('app/events/{0}.py'.format(event), 'w+')

            f.write('""" A {0} Event """\n'.format(event))
            f.write('from events import Event\n\n')
            f.write('class {0}(Event):\n    """ {0} Event Class """\n\n    subscribe = []\n\n    def __init__(self):\n        """ Event Class Constructor """\n        pass\n\n    def handle(self):\n        """ Event Handle Method """\n        pass\n'.format(event))

            self.info('Event Created Successfully!')
        else:
            self.error('Event Already Exists!')