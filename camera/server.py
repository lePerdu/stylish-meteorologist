import sys

import dotenv

from flask import Flask

from camera import capture
from camera import weather
from camera import clothing

dotenv.load_dotenv()

app = Flask(__name__)


@app.route('/checkClothing', methods=('GET',))
def check_clothing():
    cur_weather = weather.get_weather()

    image = capture.capture_image()

    result = clothing.wearing_warm_clothes(image)
    if result is None:
        return {
            'success': False,
            'error': "No person detected",
        }
    else:
        wearing_coat, wearing_pants = result
        return {
            'success': True,
            'temp': cur_weather.temp,
            'min_temp': cur_weather.min_temp,
            'max_temp': cur_weather.max_temp,
            'is_raining': cur_weather.is_raining,
            'wearing_coat': wearing_coat,
            'wearing_pants': wearing_pants,
        }


if __name__ == '__main__':
    app.run()
