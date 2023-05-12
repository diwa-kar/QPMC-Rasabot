import requests
import xmltodict
import json
from flatten_json import flatten

from suds.client import Client
from suds.transport.https import HttpAuthenticated


username = 'KAAR'
password = 'Qpmck@@r098'



# ************************************************* api from QPMC system *****************************************************************


def pending_prlist_qpmc():

    url = 'http://hqs4hdm01.qpmc.qa:8000/sap/bc/srt/wsdl/flv_10002A1011D1/bndg_url/sap/bc/srt/scs/sap/zsd_pr_pending_list?sap-client=200'

    transport = HttpAuthenticated(username=username, password=password)
    client = Client(url,transport=transport)
    result = client.service.ZmmPrPendingListFm('ahamed')
    listofobj = result[0]
    pendingpr = ['PR '+str(i.Banfn) for i in listofobj]


    return pendingpr



# ************************************************* api from QPMC system *****************************************************************