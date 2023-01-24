from app import app
from unittest import TestCase

class ForexConverterTestCase(TestCase):
    def test_root_route(self):
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<title>Forex Converter Form</title>', html)
            self.assertIn('<h1>Forex Converter</h1>', html)



    def test_currency_converter(self):
        with app.test_client() as client:
            req = client.post("/convert", data={
                "curr_from": "USD",
                "curr_to": "USD",
                "amount": "100"
            })
            resp = req.get_data(as_text=True)

            self.assertIn('<title>Forex Converter Result</title>', resp)
            self.assertIn('<h3>Converted From United States dollar:</h3>', resp)
            self.assertIn('<span class="amt-to">100.0</span>', resp)
            

    def test_redirect(self):
        with app.test_client() as client:
            req = client.post("/convert", data={
                "curr_from": "ASDF",
                "curr_to": "USD",
                "amount": "100"
            })
            resp = req.get_data(as_text=True)

            self.assertEqual(req.status_code, 302)





            
