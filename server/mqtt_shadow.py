#This file should be run after running dustServer.py at the same PC
import time
import json
import sys
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient  # need to install AWSIoTPythonSDK via pip

Client_ID = "CoAP_Client"
Thing_Name = "IoT_System"  #Device ID
Host_Name = "a2zom7jv3fdwvd-ats.iot.ap-southeast-2.amazonaws.com"   #End Point
Root_CA = "./cert2/RootCA.crt"
Private_Key = "./cert2/b603b692cf-private.pem.key"
Cert_File = "./cert2/b603b692cf-certificate.pem.crt"

Client = AWSIoTMQTTShadowClient(Client_ID)
Client.configureEndpoint(Host_Name, 8883)
Client.configureCredentials(Root_CA, Private_Key, Cert_File)
Client.configureConnectDisconnectTimeout(10)
Client.configureMQTTOperationTimeout(5)
Client.connect()

Device = Client.createShadowHandlerWithName(Thing_Name, True)

def Callback_func(payload, responseStatus, token):
    print()
    print('UPDATE: $aws/things/' + Thing_Name + '/shadow/update/#')
    print("payload = " + payload)
    print("responseStatus = " + responseStatus)
    print("token = " + token)

def main(minor_input):
    while True:
        fp = open("dustDat.txt", "r+")
        #line_list=[]
        line_tmp = json.dumps({"data": "No DATA"})
        while True:
            line = fp.readline()
            if not line:    # If line is last line
                break
        
            #Save last selected data to line_tmp
            dic_ln = json.loads(line)
            if int(dic_ln['minor_num']) == int(minor_input):
                #line_list.append(json.dumps(dic_ln))
                line_tmp = line

        #msg = {"state": {"reported": {"dust_data": line_list}}}
        msg = {"state": {"reported": {"dust_data": json.loads(line_tmp)}}}
        Device.shadowUpdate(json.dumps(msg), Callback_func, 5)

        fp.close
        time.sleep(10)

if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1])   # sys.argv[1] : minor_num (unique number of bus station)