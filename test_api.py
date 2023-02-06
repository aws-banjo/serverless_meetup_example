import requests

data = {"meetup_id": "amazon-web-services-dmv"}
api_endpoint = "YOUR ENDPOINT"

# IF you use IAM based auth , use the following code instead
# from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

# auth = BotoAWSRequestsAuth(
#     aws_host="FUNCTION URL WITHOUT https:// and last /",
#     aws_region="us-east-1",
#     aws_service="lambda",
# )
#resp = requests.post(api_endpoint, json=data, auth=auth)


# Non IAM based Auth
resp = requests.post(api_endpoint, json=data)
print(resp.json())
