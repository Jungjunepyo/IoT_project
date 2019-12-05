import requests
import json

host_lambda='https://cbqz37du17.execute-api.ap-northeast-2.amazonaws.com/default/ServoMotor'

data={"dust_density": 10.0123, "minor_num": 1}

json_data = json.dumps(data)

response = requests.post(host_lambda, json_data, headers=None)

print response.json()
