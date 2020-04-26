import telegram_handler


def lambda_handler(event, context):
    data = telegram_handler.convert(event)
    telegram_handler.default_handler(data)
    return {
        'statusCode': 200,
        'body': ""
    }