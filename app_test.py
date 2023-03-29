import unittest

from unittest import mock

import app

#TODO: Write more unittests 

class AppTest(unittest.TestCase):

    def test_token(self):
        args1 = mock.Mock()
        args1.access_token = 'fake_token'
        self.assertEqual(
            app.get_header(args1),
            {"Authorization": f"Bearer fake_token" })

    def test_creds_json(self):
        args1 = mock.Mock()
        args1.access_token = None
        args1.creds_json= 'fake.json'
        with mock.patch("builtins.open", mock.mock_open(
            read_data='{"access-token": "fake_token"}')):     
            self.assertEqual(
                app.get_header(args1),
                {"Authorization": f"Bearer fake_token" }) 


    def test_movie_listing(self):
        movies = [{'_id':"1a"},{'_id':"1b"}]
        with mock.patch.object(app, '_make_api_request') as mock_request:
            mock_request.return_value = movies
            self.assertEqual(app.list_movies({}), movies)


    def test_movie_id(self):
        movie = [{'_id':"1b", "name": "movieB"}]
        with mock.patch.object(app, '_make_api_request') as mock_request:
            mock_request.return_value = movie
            self.assertEqual(app.retrieve_movie({}, "fake_id", field_filter="name"),
            {"name" : "movieB"})

    def test_quote_listing(self):
        quotes = [{'_id':"1a","quote":"frodo said this"},{'_id':"1b", "quote":"bilbo said this"}]
        with mock.patch.object(app, '_make_api_request') as mock_request:
            mock_request.return_value = quotes
            self.assertEqual(app.list_quotes({}, "fake_id", search_filter="quote,frodo"),
            [{'_id':"1a","quote":"frodo said this"}])  

if __name__ == '__main__':
    unittest.main()