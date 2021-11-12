import os
import boto3
from chalice import Chalice, Response
from chalicelib.data_model import InputData

app = Chalice(app_name='globaltempapi')

table_name = os.environ.get('TABLE_NAME', 'globaltemperature')
_dynamo_table_client = boto3.resource('dynamodb').Table(table_name)


@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/health')
def health_ping():
    return Response(body={'status': 'OK'}, status_code=200)


@app.route('/download_record/{country}', methods=['POST'])
def get_record(country):
    get_record_json = app.current_request.json_body
    start_date = get_record_json.get('start', None)
    end_date = get_record_json.get('end', None)
    record_limit = get_record_json.get('limit', 100)
    record_country = country
    try:
        data_from_table = _dynamo_table_client.query(
            TableName="globaltemperature",
            KeyConditionExpression="#DDB_Country = :pkey and #DDB_dt BETWEEN :skey_start and :skey_end",
            ExpressionAttributeValues={
                ":pkey": record_country,
                ":skey_start": start_date,
                ":skey_end": end_date
            },
            ExpressionAttributeNames={
                "#DDB_Country": "Country",
                "#DDB_dt": "dt"
            },
            Limit=record_limit,
        )
        return data_from_table
    except:
        Response('!!Error retrieving data from table')

@app.route('/insert_record', methods=['POST'])
def insert_record():
    try:
        validation_response = InputData(**app.current_request.json_body)
        print(validation_response)
    except:
        return Response(body="Error validation json body that needs to be inserted into dynamodb")
    _dynamo_table_client.put_item(Item=app.current_request.json_body)
    return Response(body='data inserted into table')


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#