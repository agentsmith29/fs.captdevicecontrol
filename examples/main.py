import logging
import sys
import os

sys.path.append('../src/')

from PySide6.QtWidgets import QApplication
from rich.logging import RichHandler


import src.CaptDeviceControl as CaptDevice


if __name__ == "__main__":

    def setup_logging():
        for log_name, log_obj in logging.Logger.manager.loggerDict.items():
            if log_name != '<module name>':
                log_obj.disabled = True
        # Format the Rich logger
        FORMAT = "%(message)s"
        logging.basicConfig(
            level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[
                RichHandler(rich_tracebacks=True)
            ]
        )


    app = QApplication()
    setup_logging()

    conf = CaptDevice.Config()
    conf.load("config.yaml")


    model = CaptDevice.Model(conf)
    controller = CaptDevice.Controller(model)
    window = CaptDevice.View(model, controller)

    window.show()

    sys.exit(app.exec())