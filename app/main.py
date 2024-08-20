import requests
from flask import Flask, jsonify, abort
from app.config import BASE_URLS, WINDOW_SIZE

app = Flask(__name__)


cache = {
    'p': [],
    'f': [],
    'e': [],
    'r': []
}

def fetch_numbers(number_type):
    #Fetch numbers from the test server based on type.
    url = BASE_URLS.get(number_type)

    if not url:
        return []
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('numbers', [])
    except requests.RequestException as e:
        app.logger.error(f"Error fetching numbers for {number_type}: {e}")

        return []

def get_numbers_from_cache(number_type):
    
    numbers = fetch_numbers(number_type)
    if len(numbers) > WINDOW_SIZE:
        numbers = numbers[-WINDOW_SIZE:]
    cache[number_type] = numbers
    return numbers

@app.route('/numbers/<string:numberid>', methods=['GET'])
def get_average(numberid):
    
    valid_ids = {'p', 'f', 'e', 'r'}
    if numberid not in valid_ids:
        abort(400, description=f"Invalid number ID {numberid}")

    numbers = get_numbers_from_cache(numberid)

    if not numbers:
        abort(404, description=f"No numbers found for ID {numberid}")

    average = sum(numbers) / len(numbers)
    return jsonify({
        'numberid': numberid,
         'numbers': numbers,
        'windowPrevState': [],
        'windowCurrState': numbers,
        'avg': average
    }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876, debug=False)
