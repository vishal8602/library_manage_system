import logging

logger = logging.getLogger(__name__)


class SRCException(Exception):
    """Exception raised by every module in the SRC package."""

    def __init__(self, msg=None):
        """

        Args:
            msg (str): human friendly error message.
        """

        if msg is None:
            msg = "SRC Exception"
        logger.exception(msg)
        super().__init__(msg)
