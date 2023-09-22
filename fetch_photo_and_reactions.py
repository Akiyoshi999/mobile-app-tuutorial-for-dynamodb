import boto3

from application.entities import Photo, Reaction

dynamodb = boto3.client('dynamodb')

USER = "david25"
TIMESTAMP = "2019-03-02T09:11:30"


def fetch_photo_and_ractions(username, timestamp):
    try:
        resp = dynamodb.query(
            TableName='quick-photos',
            IndexName='InvertedIndex',
            KeyConditionExpression="SK = :sk AND PK BETWEEN :reactions AND :user",
            ExpressionAttributeValues={
                ":sk": {"S": "PHOTO#{}#{}".format(username, timestamp)},
                ":user": {"S": "USER$"},
                ":reactions": {"S": "REACTION#"}
            },
            ScanIndexForward=True,
        )
    except Exception as e:
        print("Index is still backfilling. Please trye again in a moment.")
        print(e)
        return False

    items = resp['Items']
    items.reverse()

    photo = Photo(items[0])
    photo.reactions = [Reaction(item) for item in items[1:]]

    return photo


photo = fetch_photo_and_ractions(USER, TIMESTAMP)

if photo:
    print(photo)
    for reaction in photo.reactions:
        print(reaction)
