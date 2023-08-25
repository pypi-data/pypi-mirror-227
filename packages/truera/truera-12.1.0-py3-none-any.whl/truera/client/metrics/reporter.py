from abc import ABC
import datetime
import logging
from typing import Mapping, Optional, Union

from truera.client.services.streaming_ingress_client import \
    StreamingIngressClient
from truera.client.truera_authentication import TrueraAuthentication
from truera.client.truera_workspace import TrueraWorkspace


class MetricReporter(ABC):

    def __init__(
        self,
        streaming_ingress_client: StreamingIngressClient,
        project_id: str,
        model_id: Optional[str] = None,
        logger: Optional[logging.Logger] = None
    ):
        """Class responsible for sending metrics. If `model_id` is not None, metrics will be associated with the given model."""
        self.streaming_ingress_client = streaming_ingress_client
        self.project_id = project_id
        self.model_id = model_id
        self.logger = logger or logging.getLogger(__name__)

    def sendMetrics(
        self,
        metrics: Mapping[str, float],
        *,
        time: Optional[datetime.datetime] = None
    ):
        """Send metric values at point in time.

        Args:
            metrics: Mapping of metric names to values.
            time: Datetime representing timestamp of the metric. Defaults to `datetime.utcnow()`.
        """
        if time is None:
            time = datetime.datetime.now(datetime.timezone.utc)
        if time.tzinfo is None or time.tzinfo.utcoffset(time) is None:
            self.logger.warning(
                "Provided `time` does not include timezone info. Timezone info will be set to UTC."
            )
            time = time.replace(tzinfo=datetime.timezone.utc)

        self.streaming_ingress_client.ingest_metric(
            project_id=self.project_id,
            timestamp=str(time.isoformat()),
            metrics=metrics,
            model_id=self.model_id
        )

    def send(
        self,
        metric: str,
        value: float,
        *,
        time: Optional[datetime.datetime] = None
    ):
        """Send a value for a metric at point in time.

        Args:
            metric: Name of the metric to send.
            value: Value of the metric to send.
            time: Datetime representing timestamp of the metric. Defaults to `datetime.utcnow()`.
        """
        metrics = {metric: value}
        self.sendMetrics(metrics, time=time)


def getGeneralMetricReporter(tru: TrueraWorkspace) -> MetricReporter:
    tru._ensure_project()
    return MetricReporter(
        streaming_ingress_client=tru.remote_tru.streaming_ingress_client,
        project_id=tru.current_tru.project.id,
        logger=tru.logger
    )


def getModelMetricReporter(tru: TrueraWorkspace) -> MetricReporter:
    tru._ensure_project()
    tru._ensure_model()
    return MetricReporter(
        streaming_ingress_client=tru.remote_tru.streaming_ingress_client,
        project_id=tru.current_tru.project.id,
        model_id=tru.current_tru.model.model_id,
        logger=tru.logger
    )
