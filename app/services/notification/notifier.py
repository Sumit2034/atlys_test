class Notifier:
    """we can also use SQS here to send the event"""
    @staticmethod
    async def notify(message: str):
        print(message)
