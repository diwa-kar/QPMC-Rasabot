# Importing necessary libraries

import uvicorn

from fastapi import FastAPI,File,UploadFile,Form
import pandas as pd
# from fastapi import jsonify

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request,Response
from fastapi.encoders import jsonable_encoder

from pymongo import MongoClient
import urllib


import requests
import xmltodict
import json
from flatten_json import flatten

from suds.client import Client
from suds.transport.https import HttpAuthenticated

username = 'KAAR'
password = 'Qpmck@@r098'

# connection string for mongoDB

# mongodb_uri = 'mongodb+srv://Amudhesh_KT:' + \
#     urllib.parse.quote('Amudhesh@78') + \
#             '@recommendationsystem.bst8vqw.mongodb.net/test'
# port = 8001
# client = MongoClient(mongodb_uri, port)
# db = client["RecommendationSystem"]


mongodb_uri = 'mongodb+srv://Bharathkumarkaar:1874924vbk@rasachatbot.ibvkwut.mongodb.net/test'
client = MongoClient(mongodb_uri)




# Initializing the fast API server

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

#defining the model inputs

class User(BaseModel):
    prno : int
    pritemno : int


@app.get('/')
async def index():
    return {'message':'hello, world'}

@app.get('/welcome')
async def welcome():
    return {'message':'Welcome, Mate!'}


@app.get('/qpmc_pending_pr')
async def pending_pr():

    url = 'http://hqs4hdm01.qpmc.qa:8000/sap/bc/srt/wsdl/flv_10002A1011D1/bndg_url/sap/bc/srt/scs/sap/zsd_pr_pending_list?sap-client=200'

    transport = HttpAuthenticated(username=username, password=password)
    client = Client(url,transport=transport)
    result = client.service.ZmmPrPendingListFm('ahamed')
    listofobj = result[0]
    pendingpr = ['PR '+str(i.Banfn) for i in listofobj]

    print(pendingpr)

    return{'pending_pr': pendingpr}


@app.get('/qpmc_pending_pr_items')
async def pending_pr_items(prno:int):

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

    print(itemlist)


    return {"pr_item_list": itemlist}


@app.get('/qpmc_pending_pr_item_description')
async def qpmc_pending_pr_item_description(prno:int, pritemno:int):

    url = f'http://172.16.195.52:8000/sap/opu/odata/sap/API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem(PurchaseRequisition=\'{prno}\',PurchaseRequisitionItem=\'{pritemno}\')?sap-client=200'
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
    desc = {}
    desc['Purchase_Requisition_Number'] = flatjs['entry_content_m:properties_d:PurchaseRequisition']
    desc['Purchase_Requisition_Item_Number'] = flatjs['entry_content_m:properties_d:PurchaseRequisitionItem']
    desc['Purchase_Requisition_Release_Status'] = flatjs['entry_content_m:properties_d:PurReqnReleaseStatus']
    desc['Purchase_Requisition_Item_Text'] = flatjs['entry_content_m:properties_d:PurchaseRequisitionItemText']
    desc['Purchase_Requisition_Material_Group'] = flatjs['entry_content_m:properties_d:MaterialGroup']
    desc['Requested_Quantity'] = flatjs['entry_content_m:properties_d:RequestedQuantity']
    desc['Base_Unit'] = flatjs['entry_content_m:properties_d:BaseUnit']
    desc['Purchase_Requisition_Price'] = flatjs['entry_content_m:properties_d:PurchaseRequisitionPrice']
    desc['Plant'] = flatjs['entry_content_m:properties_d:Plant']
    desc['Company_Code'] = flatjs['entry_content_m:properties_d:CompanyCode']
    desc['Processing_Status'] = flatjs['entry_content_m:properties_d:ProcessingStatus']
    desc['Delivery_Date'] = flatjs['entry_content_m:properties_d:DeliveryDate']
    desc['Creation_Date'] = flatjs['entry_content_m:properties_d:CreationDate']
    

    pritemdesc = desc

    for i in pritemdesc.keys():
        if i == "Purchase_Requisition_Number":
            PRnumber = pritemdesc[i]
        elif i == "Purchase_Requisition_Item_Number":
            PRItemNumber = pritemdesc[i]
        elif i == "Purchase_Requisition_Release_Status":
            PRItemStatus = pritemdesc[i]
        elif i == "Purchase_Requisition_Item_Text":
            PRItemText = pritemdesc[i]
        elif i == "Purchase_Requisition_Material_Group":
            PRMaterialGroup = pritemdesc[i]
        elif i == "Requested_Quantity":
            PRQuantity = pritemdesc[i]
        elif i == "Base_Unit":
            PRBaseUnit = pritemdesc[i]
        elif i == "Purchase_Requisition_Price":
            PRPrice = pritemdesc[i]
        elif i == "Plant":
            PRPlant = pritemdesc[i]
        elif i == "Company_Code":
            PRCompanyCode = pritemdesc[i]
        elif i == "Processing_Status":
            PRProcessingStatus = pritemdesc[i]
        elif i == "Delivery_Date":
            PRDeliveryDate = pritemdesc[i]
        elif i == "Creation_Date":
            PRCreationDate = pritemdesc[i]
    
    if PRItemStatus == "01":
        status = "Saved, not yet released"
    elif PRItemStatus == "02":
        status = "Released"
    elif PRItemStatus == "03":
        status = "Partially ordered"
    elif PRItemStatus == "04":
        status = "Completely ordered"
    elif PRItemStatus == "05":
        status = "Deleted"
    elif PRItemStatus == "06":
        status = "Manually set to Closed"
    elif PRItemStatus == "07":
        status = "Technically completed"
    elif PRItemStatus == "08":
        status = "Manually set to Locked"
    elif PRItemStatus == "09":
        status = "Sent"
    elif PRItemStatus == "10":
        status = "Partially invoiced"
    elif PRItemStatus == "11":
        status = "Completely invoiced"
    elif PRItemStatus == "12":
        status = "Manually set to Archived"
    if PRProcessingStatus == "N":
        Pstatus = "Not edited"
    elif PRProcessingStatus == "B":
        Pstatus = "PO created"
    elif PRProcessingStatus == "A":
        Pstatus = "RFQ created"
    elif PRProcessingStatus == "K":
        Pstatus = "Contract created"
    elif PRProcessingStatus == "L":
        Pstatus = "Scheduling aggrement created"
    elif PRProcessingStatus == "S":
        Pstatus = "Service entry sheet created"
    elif PRProcessingStatus == "D":
        Pstatus = "Deployment STR"
    elif PRProcessingStatus == "E":
        Pstatus = "RFQ sent to external system for sourcing"

    new_line = "\n"
    details = {
            "Purchase Requisition Number": PRnumber,
            "Purchase Requisition Item Number": PRItemNumber,
            "Purchase_Requisition_Release_Status": f"{ PRItemStatus} - {status}",
            "Purchase Requisition Item Text": PRItemText,
            "Purchase_Requisition_Material_Group": PRMaterialGroup,
            "Requested_Quantity": PRQuantity,
            "Base_Unit": PRBaseUnit,
            "Purchase_Requisition_Price": PRPrice,
            "Plant": PRPlant,
            "Company_Code": PRCompanyCode,
            "Processing_Status": f"{PRProcessingStatus} - {Pstatus}",
            "Creation_Date": PRCreationDate,
            "Delivery_Date": PRDeliveryDate,
        }


    return { "item_desc" : details }



@app.post('/qmpc_pending_pr_item_info')
async def qmpc_pending_pr_item_info(request:Request):

    data=await request.json()
    prno=data['prno'].split(' ')[-1]

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

    items_list=[]

    for i in itemlist:
        a = i.split()[-1]
        items_list.append(a)

    item_list_description = {}

    for i in items_list:
        url = f'http://172.16.195.52:8000/sap/opu/odata/sap/API_PURCHASEREQ_PROCESS_SRV/A_PurchaseRequisitionItem(PurchaseRequisition=\'{prno}\',PurchaseRequisitionItem=\'{i}\')?sap-client=200'
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
        desc = {}
        desc['Purchase_Requisition_Number'] = flatjs['entry_content_m:properties_d:PurchaseRequisition']
        desc['Purchase_Requisition_Item_Number'] = flatjs['entry_content_m:properties_d:PurchaseRequisitionItem']
        desc['Purchase_Requisition_Release_Status'] = flatjs['entry_content_m:properties_d:PurReqnReleaseStatus']
        desc['Purchase_Requisition_Item_Text'] = flatjs['entry_content_m:properties_d:PurchaseRequisitionItemText']
        desc['Purchase_Requisition_Material_Group'] = flatjs['entry_content_m:properties_d:MaterialGroup']
        desc['Requested_Quantity'] = flatjs['entry_content_m:properties_d:RequestedQuantity']
        desc['Base_Unit'] = flatjs['entry_content_m:properties_d:BaseUnit']
        desc['Purchase_Requisition_Price'] = flatjs['entry_content_m:properties_d:PurchaseRequisitionPrice']
        desc['Plant'] = flatjs['entry_content_m:properties_d:Plant']
        desc['Company_Code'] = flatjs['entry_content_m:properties_d:CompanyCode']
        desc['Processing_Status'] = flatjs['entry_content_m:properties_d:ProcessingStatus']
        desc['Delivery_Date'] = flatjs['entry_content_m:properties_d:DeliveryDate']
        desc['Creation_Date'] = flatjs['entry_content_m:properties_d:CreationDate']
        item_list_description["PR item "+ i] = desc
    print(item_list_description)

    return item_list_description


@app.get('/qpmc_pending_pr_approval')
async def qpmc_pending_pr_approval(prno:int):

    url = 'http://hqs4hdm01.qpmc.qa:8000/sap/bc/srt/wsdl/flv_10002A1011D1/bndg_url/sap/bc/srt/scs/sap/zsd_pr_appr_rej?sap-client=200'
    transport = HttpAuthenticated(username=username, password=password)
    client_sap = Client(url,transport=transport)

    text = ""

    result = client_sap.service.ZmmPrApprRejFm('A',f'{prno}','ahamed')

    Status_code = result["ExStatus"]

    print(f"{Status_code}")

    if Status_code == "ERROR":

        text =f"PR {prno} is already approved/rejected" 


    elif Status_code == "APPROVED":

        db = client["QPMC_RasaChatbot"]
        collection = db["Approved_PR"]
        document = {"Purchase Requisition Number": "PR "+f"{prno}", "Status":"Approved"}
        res = collection.insert_one(document)

        text =f"PR {prno} is Approved successfully" 

    

    return {"result" : result, "text":text}

@app.get('/qpmc_pending_pr_reject')
async def qpmc_pending_pr_reject(prno:int):

    url = 'http://hqs4hdm01.qpmc.qa:8000/sap/bc/srt/wsdl/flv_10002A1011D1/bndg_url/sap/bc/srt/scs/sap/zsd_pr_appr_rej?sap-client=200'
    transport = HttpAuthenticated(username=username, password=password)
    client_sap = Client(url,transport=transport)


    result = client_sap.service.ZmmPrApprRejFm('R',f'{prno}','ahamed')

    Status_code = result["ExStatus"]

    print(f"{Status_code}")

    text = ""

    if Status_code == "ERROR":
        text =f"PR {prno} is already approved/rejected" 

    elif Status_code == "REJECTED":
            
        db = client["QPMC_RasaChatbot"]
        collection = db["Rejected_PR"]
        document = {"Purchase Requisition Number": "PR "+f"{prno}", "Status":"Rejected"}
        res = collection.insert_one(document)

        text =f"PR {prno} is Approved successfully"


    return {"result":result, "text": text}


@app.get('/qpmc_approved_pr_list_mongo')
async def qpmc_approved_pr_list_mongo():

    db = client["QPMC_RasaChatbot"]
    collection = db["Approved_PR"]
    a=collection.find()

    approved_pr_list = []

    for i in a:
        approved_pr_list.append(i['Purchase Requisition Number'])


    return approved_pr_list


@app.get('/qpmc_rejected_pr_list_mongo')
async def qpmc_rejected_pr_list_mongo():

    db = client["QPMC_RasaChatbot"]
    collection = db["Rejected_PR"]
    a=collection.find()

    rejected_pr_list=[]

    for i in a:
        rejected_pr_list.append(i['Purchase Requisition Number'])



    return rejected_pr_list



if __name__ == '__main__':
    uvicorn.run(app,port=8000, log_level="info")