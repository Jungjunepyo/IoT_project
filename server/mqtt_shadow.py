#This file should be run after running dustServer.py at the same PC
import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient  # need to install AWSIoTPythonSDK via pip

Client_ID = "CoAP_Client"
Thing_Name = "IoT_System"  #Device ID
Host_Name = "a1zm4oahh01g1s-ats.iot.ap-northeast-1.amazonaws.com"   #End Point
Root_CA = "./cert2/RootCA.crt"
Private_Key = "./cert2/cc544bb473-private.pem.key"
Cert_File = "./cert2/cc544bb473-certificate.pem.crt"

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
    
while True:
    fp = open("dustDat.txt", "r+")
    line_list=[]
    while True:
        line = fp.readline()
        if not line:    # If line is last line
            break

        #Save selected data to line_list
        dic_ln = json.loads(line)
        if int(dic_ln['minor_num']) >= 1 and int(dic_ln['minor_num']) <= 3:
            line_list.append(json.dumps(dic_ln))

    msg = {"state": {"reported": {"dust_data": line_list}}}
    #print(line_list)
    Device.shadowUpdate(json.dumps(msg), Callback_func, 5)

    fp.close
    time.sleep(10)
