import logging
import requests
import re
import json
import xml.etree.ElementTree as ET


class Logger(object):

    def __init__(self):

        """

        This is also trial to make some simple logging handlers

        """

        super(Logger, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler('swager_requests.log')
        formatter = logging.Formatter('%(levelname)s - %(module)s/%(funcName)s - %(asctime)s : %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


class SwaggerRequests(Logger):

    def __init__(self):
        super(SwaggerRequests, self).__init__()
        self.base_url = 'http://petstore.swagger.io/v2/pet'

    def read_pet_data_json(self):

        with open('pet_data.json') as json_file:
            json_data = json.load(json_file)

        return json_data

    def prepare_url(self, suffix):

        """This function prepares correct url format"""

        return self.base_url.rstrip('/') + '/' + suffix.lstrip('/')

    def log_error(self, status_code):

        """This is function used for event logging of this module"""

        error_code4XX = re.compile('^4[0-9]{2}')
        error_code5XX = re.compile('^5[0-9]{2}')

        if re.search(error_code4XX, str(status_code)) is not None or \
                re.search(error_code5XX, str(status_code)) is not None:
            return 'error'
        else:
            return 'debug'

    def find_xml_element(self, xml_elements, element_to_find):

        for element in xml_elements.findall(element_to_find):
            return element.text

    def get_pet_data_json(self, suffix='/'):

        """For get pet by id use /{id} suffix"""

        url = self.prepare_url(suffix)

        header_data = {'accept': 'application/json'}
        get_response = requests.get(url, headers=header_data)

        self.logger.debug('{0} URL: {1}'.format('GET', url))

        if self.log_error(get_response.status_code) == 'debug':
            self.logger.debug('{0} RESPONSE CODE: {1}'.format('GET:JSON', get_response.status_code))
        else:
            self.logger.error('{0} ERROR RESPONSE: {1}'.format('GET:JSON', get_response.status_code))

        return get_response

    def get_pet_data_xml(self, suffix='/'):

        url = self.prepare_url(suffix)

        header_data = {'accept': 'application/xml'}
        get_response = requests.get(url, headers=header_data)

        self.logger.debug('{0} URL: {1}'.format('GET:XML', url))

        if self.log_error(get_response.status_code) == 'debug':
            self.logger.debug('{0} RESPONSE CODE: {1}'.format('GET:XML', get_response.status_code))
        else:
            self.logger.error('{0} ERROR RESPONSE: {1}'.format('GET:XML', get_response.status_code))

        return get_response

    def post_pet_data_json(self, id, pet_name, suffix):

        """This is function to add new pet data"""

        url = self.prepare_url(suffix)

        # URL logging
        self.logger.debug('{0} URL: {1}'.format('POST:JSON', url))

        json_data = self.read_pet_data_json()
        json_data['id'] = id
        json_data['name'] = pet_name

        header_data = {'content-type': 'application/json', 'accept': 'application/json'}

        post_response = requests.post(url, json=json_data, headers=header_data)
        id, name = json.loads(post_response.text)['id'], json.loads(post_response.text)['name']

        if self.log_error(post_response.status_code) == 'debug':
            self.logger.debug('{0} RESPONSE CODE: {1}'.format('POST:JSON', post_response.status_code))
        else:
            self.logger.error('{0} ERROR RESPONSE: {1}'.format('POST:JSON', post_response.status_code))

        self.logger.debug('{0} DATA: {1} "id": {2}, "name": {3} {4}'.format('POST:JSON', '{', id, pet_name, '}'))

        return post_response

    def post_pet_data_xml(self,id, pet_name, suffix):

        url = self.prepare_url(suffix)

        # URL logging
        self.logger.debug('{0} URL: {1}'.format('POST:XML', url))

        xml_tree = ET.parse('pet_data.xml')
        xml_tree.find('.//name').text = pet_name
        xml_tree.find('.//id').text = id
        root = xml_tree.getroot()

        xml_data = ET.tostring(root).decode()
        header_data = {'content-type': 'application/xml', 'accept': 'application/xml'}
        post_response = requests.post(url, data=xml_data, headers=header_data)

        if self.log_error(post_response.status_code) == 'debug':
            self.logger.debug('{0} RESPONSE CODE: {1}'.format('POST:XML', post_response.status_code))
        else:
            self.logger.error('{0} ERROR RESPONSE: {1}'.format('POST:XML', post_response.status_code))

        self.logger.debug('{0} DATA: {1} "id": {2}, "name": {3} {4}'.format('POST:XML', \
            '{', xml_tree.find('.//id').text, xml_tree.find('.//name').text, '}'))

        return post_response


        # raise Exception('This need to be completed with xml POST')
        # raise NotImplementedError('This need to be completed with xml POST')

    def put_request(self):

        """This function updates existing pet data with new name"""

        raise Exception('This is not yet completed, xml and json PUT need to be coded ')

if __name__ == '__main__':
    pass