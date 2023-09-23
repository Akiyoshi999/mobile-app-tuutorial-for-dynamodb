import datetime
import boto3

dynamodb = boto3.client('dynamodb')


FOLLOWED_USER = 'tmartinez'
FOLLOWING_USER = 'john42'
TABLE_NAME = "quick-photos"


def follow_user(followed_user, following_user):
    user = "USER#{}".format(followed_user)
    friend = "#FRIEND#{}".format(following_user)
    user_metadata = "#METADATA#{}".format(followed_user)
    friend_user = "USER#{}".format(following_user)
    friend_metadata = "#METADATA#{}".format(following_user)
    try:
        resp = dynamodb.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": TABLE_NAME,
                        "Item": {
                            "PK": {"S": user},
                            "SK": {"S": friend},
                            "followedUser": {"S": FOLLOWED_USER},
                            "follwingUser": {"S": FOLLOWING_USER},
                            "timestamp": {"S": datetime.datetime.now().isoformat()},
                        },
                        "ConditionExpression": "attribute_not_exists(SK)",
                        "ReturnValuesOnConditionCheckFailure": "ALL_OLD"
                    }
                },
                {
                    "Update": {
                        "TableName": TABLE_NAME,
                        "Key": {"PK": {"S": user}, "SK": {"S": user_metadata}},
                        "UpdateExpression": "SET followers = followers + :1",
                        "ExpressionAttributeValues": {":1": {"N": "1"}},
                        "ReturnValuesOnConditionCheckFailure": "ALL_OLD"
                    }
                },
                {
                    "Update": {
                        "TableName": TABLE_NAME,
                        "Key": {"PK": {"S": friend_user}, "SK": {"S": friend_metadata}},
                        "UpdateExpression": "SET following = following + :1",
                        "ExpressionAttributeValues": {":1": {"N": "1"}},
                        "ReturnValuesOnConditionCheckFailure": "ALL_OLD"
                    }
                }
            ]
        )
        print("user {} is now following user {}".format(
            following_user, followed_user))
        return True
    except Exception as e:
        print(e)
        print("Could not add follow relationship")


follow_user(FOLLOWED_USER, FOLLOWING_USER)
