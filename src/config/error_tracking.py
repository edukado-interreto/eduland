import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .utils import Environment


def setup_bugsink(config, environment: Environment):
    sentry_sdk.init(
        dsn=config.BUGSINK_DSN,
        release=config.COMMIT_HASH,
        server_name=config.HOSTNAME,
        environment=environment.value,
        integrations=[DjangoIntegration(signals_spans=False)],
        send_default_pii=True,
        max_request_body_size="always",
        # Don't event types which are not supported by Bugsink:
        traces_sample_rate=0,
        send_client_reports=False,
        auto_session_tracking=False,
    )
