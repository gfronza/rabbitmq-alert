#! /usr/bin/python2
# -*- coding: utf8 -*-

import logging
import mock
import unittest

from rabbitmqalert import logger


class LoggerTestCase(unittest.TestCase):

    def setUp(self):
        logger.handlers_real = logger.handlers

    def tearDown(self):
        logger.handlers = logger.handlers_real

    def test_get_logger_returns_logger(self):
        logger.handlers = mock.MagicMock()

        the_logger = logger.Logger()
        self.assertIsInstance(the_logger.get_logger(), type(logging.getLogger()))

    def test_get_logger_returns_same_logger_instance_after_consecutive_calls(self):
        logger.handlers = mock.MagicMock()

        # same instances from same logger instance
        the_logger = logger.Logger()
        self.assertIs(the_logger.get_logger(), the_logger.get_logger())

        # same instances from different logger instances
        the_logger2 = logger.Logger()
        self.assertIs(the_logger.get_logger(), the_logger2.get_logger())


if __name__ == "__main__":
    unittest.main()
