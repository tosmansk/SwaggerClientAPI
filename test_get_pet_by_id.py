import unittest
import logging
from SwaggerClientAPI.swagger_requests import SwaggerRequests
from xml.etree import ElementTree

class GetRequestTest(unittest.TestCase):

    def setUp(self):
        self.make_request = SwaggerRequests()
        self.make_request.post_pet_data_json('1', 'Luki', '/')

    def test_get_json(self):

        """This function validates GET json response"""

        _json_response = self.make_request.get_pet_data_json('/1')

        self.assertEqual(_json_response.json()['name'], 'Luki')

    def test_get_xml(self):

        """This function uses ElementTree to parse xml response and validates xml response"""

        _xml_reponse = self.make_request.get_pet_data_xml('/1')
        _xml_elements = ElementTree.fromstring(_xml_reponse.text)
        self.assertEqual(self.make_request.find_xml_element(_xml_elements, 'name'), 'Luki')

    """
    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger(__name__)
        cls.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler('get_pet_by_id.log')
        formatter = logging.Formatter('%(levelname)s - %(module)s/%(funcName)s - %(asctime)s : %(message)s')
        file_handler.setFormatter(formatter)
        cls.logger.addHandler(file_handler)

    @classmethod
    def setResult(cls, amount, errors, failures, skipped):
        cls.amount, cls.errors, cls.failures, cls.skipped = \
            amount, errors, failures, skipped

    def tearDown(self):
        amount = self.currentResult.testsRun
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        skipped = self.currentResult.skipped
        self.setResult(amount, errors, failures, skipped)

    @classmethod
    def tearDownClass(cls):
        cls.logger.info('TEST RESULTS:\nrun: ' + str(cls.amount) + '\n' \
                + "errors: " + str(len(cls.errors)) + '\n' \
                + "failures: " + str(len(cls.failures)) + '\n' \
                + "success: " + str(cls.amount - len(cls.errors) - len(cls.failures)) + '\n'
                + "skipped: " + str(len(cls.skipped)) + '\n')

    def run(self, result=None):
        self.currentResult = result # remember result for use in tearDown
        unittest.TestCase.run(self, result) # call superclass run method
        
    """

if __name__ == '__main__':
    unittest.main()






