"""Clothing detection code."""

import boto3

rekognition = boto3.client('rekognition')

# TODO Allow this to be set in .env?
MIN_CONFIDENCE = 80

PERSON_LABELS = [
    'Person',
    'Human',
    'Man',
    'Woman',
]

COAT_LABELS = [
    'Coat',
    'Jacket',
    'Overcoat',
    'Sweater',
    'Sweatshirt',
    'Long Sleeve',
]

# TODO Rekognition doesn't really return these labels, so we don't check for
# them
PANTS_LABELS = [
    'Pants',
    'Jeans',
    'Slacks',
]

SHORTS_LABELS = [
    'Short',
    'Skirt',
]


class DetectionError(Exception):
    pass


def has_object_type(labels, clothing):
    return any((l['Name'] in clothing) for l in labels['Labels'])


def has_person(labels):
    return has_object_type(labels, PERSON_LABELS)


def wearing_coat(labels):
    return has_object_type(labels, COAT_LABELS)


def wearing_pants(labels):
    # Pants detection is a bit finicky, so also check for shorts and skirts
    has_long = has_object_type(labels, PANTS_LABELS)
    has_short = has_object_type(labels, SHORTS_LABELS)
    # Bias towards having long pants if nothing is detected
    # (the coat is kind of more important anyway)
    return has_long or not has_short


def wearing_warm_clothes(image_bytes):
    """Gets a summary of the clothing detected in the image.
    Returns:
        Tuple of (wearing_coat, wearing_pants) or None if there is no person
        detected in the image.
    """

    labels = rekognition.detect_labels(
        Image={'Bytes': image_bytes},
        MinConfidence=MIN_CONFIDENCE)

    print()

    for l in labels['Labels']:
        print(f"{l['Confidence']:0.0f}\t{l['Name']}")

    print()

    if has_person(labels):
        coat, pants = wearing_coat(labels), wearing_pants(labels)
        if coat:
            print("Wearing coat")
        if pants:
            print("Wearing long pants")
        return coat, pants
    else:
        print("No person detected")
        return None
