import sys

import dotenv

import capture
import clothing
import weather

# Load AWS credentials from the .env file
dotenv.load_dotenv()


def main():
    cur_weather = weater.get_weather()

    print(f"Temperature: {cur_weather.cur_temp}")
    if cur_weather.is_raining:
        print("Raining")

    while True:
        input()
        image = capture.capture_image()
        try:
            if clothing.wearing_warm_clothes(image):
                print("Wearing warm clothes")
            else:
                print("Not waring warm clothes")
        except clothing.DetectionError as e:
            print(str(e), file=sys.stderr)


if __name__ == '__main__':
    main()
