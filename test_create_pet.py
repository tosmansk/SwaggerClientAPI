import unittest
from SwaggerClientAPI.swagger_requests import SwaggerRequests

class CreatePet(unittest.TestCase):

    def setUp(self):
        self.make_request = SwaggerRequests()
        # pet_model = PetModel(0, category='cat')
        # self.make_request.post_pet_data_json(pet_model, '/')

    def test_post_request_json(self):
        post_response = self.make_request.post_pet_data_json('1', 'Luki', '/')
        print(post_response.json())
        self.assertEqual(post_response.status_code, '200')

