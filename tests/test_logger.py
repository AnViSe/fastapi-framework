import logging
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch
from fastapi_framework.logger import logging_formatter, get_logger, logging_handler


class LoggerTest(TestCase):
    def test_logging_format(self):
        self.assertIsInstance(logging_formatter, logging.Formatter)
        self.assertEqual("[%(asctime)s] [%(levelname)s] %(message)s", logging_formatter._fmt)

    @patch("fastapi_framework.logger.LOG_LEVEL")
    @patch("fastapi_framework.logger.logging_handler")
    @patch("logging.getLogger")
    def test_get_logger(self, getLogger_patch: MagicMock, logging_handler_patch: MagicMock, log_level_patch: MagicMock):
        name = MagicMock()

        result = get_logger(name)

        getLogger_patch.assert_called_with(name)
        self.assertEqual(result, getLogger_patch())
        getLogger_patch().addHandler.assert_called_with(logging_handler_patch)
        getLogger_patch().setLevel.assert_called_with(log_level_patch.upper())

    def test_logging_handler(self):
        self.assertIsInstance(logging_handler, logging.StreamHandler)
        self.assertEqual(logging_handler.stream, sys.stdout)
        self.assertEqual(logging_handler.formatter, logging_formatter)
