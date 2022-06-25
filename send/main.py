import base64
from google.cloud import iot_v1

# Google Cloud Function gets triggered by PubSub event
def subscribe(event, context):
    data = base64.b64decode(event['data'])
    print(f'data in function {data}')
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path("clothworks-test","europe-west1","washing-registry","washing-actuator-device")
    if int(data) > 50:
        client.send_command_to_device(request={"name":device_path,"binary_data":data})
