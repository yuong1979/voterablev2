from django.dispatch import Signal

notify = Signal(providing_args=['sender', 'recipient', 'polltype', 'pollitem', 'tagpoll', 'pollreview', 'action', 'message'])


