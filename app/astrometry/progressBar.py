import time

class ProgressBar:
    def __init__(self,label):
        self.label = label
        print(label+": ", end='')

    def incrementAndPause(self, secs):
        self.increment()
        time.sleep(secs)

    def increment(self):
        print('.', end='', flush=True)

    def done(self):
        print('', end='\n', flush=True)

