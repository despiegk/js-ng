from unittest import TestCase
from loguru import logger
from uuid import uuid4


class BaseTests(TestCase):
    LOGGER = logger

    def setUp(self):
        print('\n')
        self.info('Test case : {}'.format(self._testMethodName))

    def tearDown(self):
        pass

    @staticmethod
    def generate_random_text():
        return str(uuid4()).replace("-", "")[:10]

    @staticmethod
    def info(message):
        BaseTests.LOGGER.info(message)
