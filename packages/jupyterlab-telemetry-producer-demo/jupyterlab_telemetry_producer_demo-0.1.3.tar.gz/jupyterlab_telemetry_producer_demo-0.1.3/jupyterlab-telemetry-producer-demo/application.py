from .handlers import RouteHandler
from jupyter_server.extension.application import ExtensionApp
from traitlets import List

class JupyterLabTelemetryProducerDemoApp(ExtensionApp):

    name = "jupyterlab_telemetry_producer_demo"

    activeEvents = List([]).tag(config=True)
    logNotebookContentEvents = List([]).tag(config=True)

    def initialize_settings(self):
        try:
            assert self.activeEvents, "The c.JupyterLabTelemetryProducerDemoApp.activeEvents configuration setting must be set."
            pass

        except Exception as e:
            self.log.error(str(e))
            raise e

    def initialize_handlers(self):
        try:
            self.handlers.extend([(r"/jupyterlab-telemetry-producer-demo/(.*)", RouteHandler)])
        except Exception as e:
            self.log.error(str(e))
            raise e