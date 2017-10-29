#! /usr/bin/python2
# -*- coding: utf8 -*-

import unittest
import mock
from . import logger


class LoggerTestCase(unittest.TestCase):
    def setUp(self):
        logger.logging_real = logger.logging
        logger.handlers_real = logger.handlers

    def tearDown(self):
        logger.logging = logger.logging_real
        logger.handlers = logger.handlers_real

    def test_debug_method_calls_log_method_with_severity_debug(self):
        logger.logging = mock.MagicMock()
        the_logger = logger.Logger()
        the_logger.log = mock.MagicMock()

        the_logger.debug("foo")
        the_logger.log.assert_called_once_with(logger.logging.DEBUG, "foo")

    def test_info_method_calls_log_method_with_severity_info(self):
        logger.logging = mock.MagicMock()
        the_logger = logger.Logger()
        the_logger.log = mock.MagicMock()

        the_logger.info("foo")
        the_logger.log.assert_called_once_with(logger.logging.INFO, "foo")

    def test_warn_method_calls_log_method_with_severity_warn(self):
        logger.logging = mock.MagicMock()
        the_logger = logger.Logger()
        the_logger.log = mock.MagicMock()

        the_logger.warn("foo")
        the_logger.log.assert_called_once_with(logger.logging.WARN, "foo")

    def test_error_method_calls_log_method_with_severity_error(self):
        logger.logging = mock.MagicMock()
        the_logger = logger.Logger()
        the_logger.log = mock.MagicMock()

        the_logger.error("foo")
        the_logger.log.assert_called_once_with(logger.logging.ERROR, "foo")

    def test_critical_method_calls_log_method_with_severity_critical(self):
        logger.logging = mock.MagicMock()
        the_logger = logger.Logger()
        the_logger.log = mock.MagicMock()

        the_logger.critical("foo")
        the_logger.log.assert_called_once_with(logger.logging.CRITICAL, "foo")

    def test_log_calls_logging_debug_method_when_severity_debug(self):
        logger.logging = mock.MagicMock()
        logger.handlers = mock.MagicMock()

        the_logger = logger.Logger()
        the_logger.log(logger.logging.DEBUG, "foo")
        logger.logging.getLogger().debug.assert_called_once_with("foo")

    def test_log_calls_logging_info_method_when_severity_info(self):
        logger.logging = mock.MagicMock()
        logger.handlers = mock.MagicMock()

        the_logger = logger.Logger()
        the_logger.log(logger.logging.INFO, "foo")
        logger.logging.getLogger().info.assert_called_once_with("foo")

    def test_log_calls_logging_warn_method_when_severity_warn(self):
        logger.logging = mock.MagicMock()
        logger.handlers = mock.MagicMock()

        the_logger = logger.Logger()
        the_logger.log(logger.logging.WARN, "foo")
        logger.logging.getLogger().warn.assert_called_once_with("foo")

    def test_log_calls_logging_warn_method_when_severity_warning(self):
        logger.logging = mock.MagicMock()
        logger.handlers = mock.MagicMock()

        the_logger = logger.Logger()
        the_logger.log(logger.logging.WARNING, "foo")
        logger.logging.getLogger().warn.assert_called_once_with("foo")

    def test_log_calls_logging_error_method_when_severity_error(self):
        logger.logging = mock.MagicMock()
        logger.handlers = mock.MagicMock()

        the_logger = logger.Logger()
        the_logger.log(logger.logging.ERROR, "foo")
        logger.logging.getLogger().error.assert_called_once_with("foo")

    def test_log_calls_logging_critical_method_when_severity_critical(self):
        logger.logging = mock.MagicMock()
        logger.handlers = mock.MagicMock()

        the_logger = logger.Logger()
        the_logger.log(logger.logging.CRITICAL, "foo")
        logger.logging.getLogger().critical.assert_called_once_with("foo")

if __name__ == "__main__":
    unittest.main()
