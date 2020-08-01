class Base:
    def __init__(self, payload):
        self.payload = payload
        self.notifications_to_send = []

    def publish(self):
        print(f'Publishing notifications!')
        pass
