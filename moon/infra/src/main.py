import base64
import json
import os
from google.cloud import iot_v1

def hello_gcs(event, context):
    data = base64.b64decode(event['data'])
    print(f'data in function {data}')
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path("clothworks-hdm","europe-west1","clothworks_hdm_aWvwsa","actuator-cloth")
    if int(data) > 50:
        client.send_command_to_device(request={"name":device_path,"binary_data":data})
