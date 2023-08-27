from specklepy.api.client import SpeckleClient
from specklepy.core.api.models import Stream
from funckle.function.handler import webhook_handler, WebhookPayload

@webhook_handler(validate_webhook=True)
def webhook(webhook: WebhookPayload, client: SpeckleClient):

    stream: Stream = client.streams.get(webhook.streamId)
    
    print(stream)

    return f"Hello, {stream.name}!!!!"
