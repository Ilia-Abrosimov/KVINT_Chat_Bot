from transitions import Machine


class Bot(object):
    states = ['asleep', 'choice of size', 'choice of payment', 'formation order']

    def __init__(self):
        self.size = None
        self.payment = None
        self.machine = Machine(model=self, states=Bot.states, initial='asleep')
        self.machine.add_transition(trigger='start', source='asleep', dest='choice of size')
        self.machine.add_transition(trigger='payment_method', source='choice of size', dest='choice of payment')
        self.machine.add_transition(trigger='approve', source='choice of payment', dest='formation order')
        self.machine.add_transition(trigger='say_bye', source='formation order', dest='asleep')
        self.machine.add_transition(trigger='stop', source='*', dest='asleep')

    def set_size(self, size):
        self.size = size
        return self.size

    def set_payment(self, payment):
        self.payment = payment
        return self.payment
