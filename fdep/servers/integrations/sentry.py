from fdep.servers.integrations import Integration


class SentryIntegration(Integration):

    def __init__(self, sentry_dsn):
        from raven import Client  # To not break the app when it's optional.
        self.sentry_dsn = sentry_dsn
        self.client = Client(sentry_dsn)

    def capture_exception(self, exc):
        self.client.captureException()
