import requests
import xmltodict
import json
from flatten_json import flatten

from suds.client import Client
from suds.transport.https import HttpAuthenticated


username = 'KAAR'
password = 'Qpmck@@r098'



# ************************************************* pr list from QPMC system *****************************************************************


def pending_prlist_qpmc():

    url = 'http://hqs4hdm01.qpmc.qa:8000/sap/bc/srt/wsdl/flv_10002A1011D1/bndg_url/sap/bc/srt/scs/sap/zsd_pr_pending_list?sap-client=200'

    transport = HttpAuthenticated(username=username, password=password)
    client = Client(url,transport=transport)
    result = client.service.ZmmPrPendingListFm('ahamed')
    listofobj = result[0]
    pendingpr = ['PR '+str(i.Banfn) for i in listofobj]


    return pendingpr



# ************************************************* pr list from QPMC system *****************************************************************

# ************************************************ pending pr item list *********************************************************************

def pending_pr_item_list_qpmc(prno):

    url = f'http://172.16.195.52:8000/sap/opu/odata/sap/API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionHeader(\'{prno}\')/to_PurchaseReqnItem?sap-client=200'
    username = 'KAAR'
    password = 'Qpmck@@r098'
    # Create a session and set the authorization header
    session = requests.Session()
    session.auth = (username, password)
    # Send a GET request to the SAP system
    response = session.get(url)
    # Print the response status code and content
    obj = response.content
    objstr = str(obj, 'UTF-8')
    obj2 = xmltodict.parse(objstr)
    js = json.dumps(obj2)
    js_obj = json.loads(js)
    flatjs = flatten(js_obj)
    itemlist=[]
    i=0
    flag = 0
    while True:
        try:
            itemlist.append(f"PR Item {flatjs[f'feed_entry_{i}_content_m:properties_d:PurchaseRequisitionItem']}") 
            i+=1
            flag = 1
        except:
            if flag:
                break
            else:
                itemlist.append(f"PR Item {flatjs[f'feed_entry_content_m:properties_d:PurchaseRequisitionItem']}")
                break
    
    
    return itemlist


# ************************************************ pending pr item list *********************************************************************