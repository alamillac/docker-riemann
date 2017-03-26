from riemann import RiemannClient

local_conf = False

rc = RiemannClient()

class RiemannSender(object):
    class Events:
        OK = 'ok'
        ERROR = 'error'
        CRITICAL = 'critical'
        WARNING = 'warning'
        UNKNOWN = 'unknown'
        READY = 'ready'
        BUSY = 'busy'

    def __init__(self, host, app):

        self.app = app
        self.base_opts = {
            'host': host,
            'ttl': 60
        }
        self.valid_states = [self.Events.OK, self.Events.ERROR, self.Events.CRITICAL, self.Events.WARNING, self.Events.UNKNOWN, self.Events.READY, self.Events.BUSY]

    def send(self, event, state, msg, notify=False, opts={}):
        if local_conf:
            return

        if state not in self.valid_states:
            state = self.Events.UNKNOWN

        if 'tags' in opts and isinstance(opts['tags'], list):
            tags = opts['tags'] + [self.app]
        else:
            tags = [self.app]

        if notify:
            tags.append('notify')

        gen_opts = {'service': event, 'state': state, 'description': msg, 'tags': tags}
        arg_send = {**self.base_opts, **opts, **gen_opts}
        try:
            rc.send(arg_send)
        except:
            print("Error enviando: ", arg_send)

    def ok(self, event, msg, **args):
        self.send(event, self.Events.OK, msg, **args)

    def error(self, event, msg, **args):
        self.send(event, self.Events.ERROR, msg, **args)

    def critical(self, event, msg, **args):
        self.send(event, self.Events.CRITICAL, msg, **args)

    def warning(self, event, msg, **args):
        self.send(event, self.Events.WARNING, msg, **args)

    def unknown(self, event, msg, **args):
        self.send(event, self.Events.UNKNOWN, msg, **args)

    def ready(self, event, msg, **args):
        self.send(event, self.Events.READY, msg, notify=False, **args)

    def busy(self, event, msg, **args):
        self.send(event, self.Events.BUSY, msg, notify=True, **args)


riemann_message = RiemannSender('pre', 'Sarah')

import time
from random import randint
while True:
    import ipdb; ipdb.set_trace()  # BREAKPOINT
    print("Ready")
    riemann_message.ready("worker 1", "Esperando trabajos", opts={'ttl': 20})
    print("Busy")
    riemann_message.busy("worker 1", "Ocupado trabajando", opts={'ttl': 20})
    time.sleep(1)

#rc.send({
#    'host': "pre",
#    'service': "worker",
#    'state': 'ok',
#    'metric': 1,
#    'description': 'Request took 2.53 seconds.',
#    'tags': ['notify', 'Sarah']
#})
