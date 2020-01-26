"""Clothing detection code."""

import boto3

rekognition = boto3.client('rekognition')

# TODO Allow this to be set in .env?
MIN_CONFIDENCE = 70

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
]

# TODO Rekognition doesn't really return these labels, so we don't check for
# them
PANTS_LABELS = [
    'Pants',
    'Jeans',
]


class DetectionError(Exception):
    pass


def has_object_type(labels, clothing):
    return any((l['Name'] in clothing) for l in labels['Labels'])


def wearing_warm_clothes(image_bytes):
    labels = rekognition.detect_labels(
        Image={'Bytes': image_bytes},
        MinConfidence=MIN_CONFIDENCE)

    if has_object_type(labels, PERSON_LABELS):
        has_coat = has_object_type(labels, COAT_LABELS)
        # has_pants = has_object_type(labels, PANTS_LABELS)

        return has_coat
    else:
        raise DetectionError("No person detected")
