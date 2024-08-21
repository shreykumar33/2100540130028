import unittest
import requests
from app.main import app  

class TestAverageCalculator(unittest.TestCase):
    BASE_URL = 'http://localhost:9876/numbers'

    def test_get_average(self):
        test_cases = {
            'p': [2, 3, 5, 7, 11],
            'f': [55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765],
            'e': [2, 4, 6, 8], 
            'r': [1, 2, 3, 4, 5]  
        }

        for numberid, expected_numbers in test_cases.items():
            with app.test_client() as client:
                response = client.get(f'{self.BASE_URL}/{numberid}')
                self.assertEqual(response.status_code, 200)

                response_json = response.get_json()
                numbers = response_json.get('numbers')
                avg = response_json.get('avg')

                expected_avg = sum(expected_numbers) / len(expected_numbers) if expected_numbers else 0


                self.assertEqual(numbers, expected_numbers, f"Numbers for ID {numberid} do not match expected values.")
                self.assertEqual(avg, expected_avg, f"Average for ID {numberid} does not match the expected value.")

                # Optionally we can print response for debugging
                print(f"Response JSON for {numberid}:", response_json)

if __name__ == '__main__':
    unittest.main()
