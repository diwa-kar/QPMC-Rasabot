# Importing necessary libraries
import xmltodict
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
import numpy as np

import requests
import json
from flatten_json import flatten

from suds.client import Client
from suds.transport.https import HttpAuthenticated
from typing import Union

import re

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
    WfRequestId:str


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



@app.get('/qmpc_pending_pr_item_info')
async def qmpc_pending_pr_item_info(prno:int):
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
        desc['Purchase Requisition Number'] = flatjs['entry_content_m:properties_d:PurchaseRequisition']
        desc['Purchase Requisition Item Number'] = flatjs['entry_content_m:properties_d:PurchaseRequisitionItem']
        desc['Purchase Requisition Release Status'] = flatjs['entry_content_m:properties_d:PurReqnReleaseStatus']
        desc['Purchase Requisition Item Text'] = flatjs['entry_content_m:properties_d:PurchaseRequisitionItemText']
        desc['Purchase Requisition Material Group'] = flatjs['entry_content_m:properties_d:MaterialGroup']
        desc['Requested Quantity'] = flatjs['entry_content_m:properties_d:RequestedQuantity']
        desc['Base Unit'] = flatjs['entry_content_m:properties_d:BaseUnit']
        desc['Purchase Requisition Price'] = flatjs['entry_content_m:properties_d:PurchaseRequisitionPrice']
        desc['Plant'] = flatjs['entry_content_m:properties_d:Plant']
        desc['Company Code'] = flatjs['entry_content_m:properties_d:CompanyCode']
        desc['Processing Status'] = flatjs['entry_content_m:properties_d:ProcessingStatus']
        desc['Delivery Date'] = flatjs['entry_content_m:properties_d:DeliveryDate']
        desc['Creation Date'] = flatjs['entry_content_m:properties_d:CreationDate']
        item_list_description["PR item "+ i] = desc
    print(item_list_description)

    return item_list_description


@app.get('/qpmc_pending_pr_approval')
async def qpmc_pending_pr_approval(prno:int):
    print(prno) 
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

        text =f"PR {prno} is Rejected successfully"


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

@app.get('/qpmc_leave_reuqest_sf')
async def qpmc_leave_reuqest_sf():

    username = 'kaaradmin@qatarprimaT1'
    password = 'Qpmc@456'

     # extranct date from the sentence
    def extract_date_from_sentence(sentence):
        pattern = r"\((.*?)\)"  # Regex pattern to match text within parentheses
        match = re.search(pattern, sentence)  # Search for the pattern in the sentence

        if match:
            date_within_parentheses = match.group(1)  # Extract the text within parentheses
            return date_within_parentheses
        else:
            return None

    # extracting words before paranthesis to find Leave Type
    def words_before_parenthesis(sentence):
        # Find the index of the opening parenthesis
        parenthesis_index = sentence.find("(")

        if parenthesis_index != -1:
            words = sentence[:parenthesis_index][:-1]
            return words
        else:
            return None

    # picking up name from the sentece 
    def pick_name_from_sentence(sentence):
        colon_index = sentence.find(":")
        
        if colon_index != -1:
            words = sentence[colon_index+2:]
            return words
        else:
            return None

    url = 'https://api2preview.sapsf.eu/odata/v2/Todo?$filter=categoryId%20eq%20%2718%27'
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

    pendingleave=[]
    i=0 
    while True:
        try:
            d={
            'Leave Id':flatjs[f'feed_entry_content_m:properties_d:todos_d:element_d:entries_d:element_{i}_d:subjectId'],
            'Employee Name':pick_name_from_sentence(flatjs[f'feed_entry_content_m:properties_d:todos_d:element_d:entries_d:element_{i}_d:subjectFullName']),
            'Leave Duration': extract_date_from_sentence(flatjs[f'feed_entry_content_m:properties_d:todos_d:element_d:entries_d:element_{i}_d:subjectFullName']),
            'Leave Type': words_before_parenthesis(flatjs[f'feed_entry_content_m:properties_d:todos_d:element_d:entries_d:element_{i}_d:subjectFullName'])
            }
            pendingleave.append(d)
            i+=1
        except: 
            break
  
    print(pendingleave)

    return pendingleave


@app.get('/qpmc_accept_leave_reuqest_sf')
async def qpmc_accept_leave_reuqest_sf(WfRequestId:str):

     # Set the SAP URL and credentials
    url = f'https://api2preview.sapsf.eu/odata/v2/approveWfRequest?wfRequestId={WfRequestId}&comment=Approved'
    username = 'kaaradmin@qatarprimaT1'
    password = 'Qpmc@456'
    # Create a session and set the authorization header
    session = requests.Session()
    session.auth = (username, password)
    # Send a GET request to the SAP system
    response = session.post(url)
    # Print the response status code and content
    print(response.status_code)
    if response.status_code == 200:
        db = client["QPMC_RasaChatbot"]
        collection = db["Approved_Leave"]
        document = {"Leave Id":f"{WfRequestId}", "Status":"Approved"}
        res = collection.insert_one(document)

    if response.status_code == 200:
        res = f"Leave Request ({WfRequestId}) has been approved"
    else:
        res = f"Leave Request ({WfRequestId}) has been already approved and moved to higher level approver"

    return res

@app.get('/qmpc_reject_leave_request_sf')
async def qpmc_reject_leave_request_sf(WfRequestId:str):

    # Set the SAP URL and credentials
    url = f'https://api2preview.sapsf.eu/odata/v2/rejectWfRequest?wfRequestId={WfRequestId}&comment=Rejected'
    username = 'kaaradmin@qatarprimaT1'
    password = 'Qpmc@456'
    # Create a session and set the authorization header
    session = requests.Session()
    session.auth = (username, password)
    # Send a GET request to the SAP system
    response = session.post(url)
    # Print the response status code and content
    print(response)
    if response.status_code == 200:
        db = client["QPMC_RasaChatbot"]
        collection = db["Rejected_Leave"]
        document = {"Leave Id":f"{WfRequestId}", "Status":"Rejected"}
        res = collection.insert_one(document)

    if response.status_code == 200:
        res = f"Leave Request ({WfRequestId}) has been rejected"
    else:
        res = f"Leave Request ({WfRequestId}) has been already rejected"


    return res


@app.get('/qpmc_approved_leave_list_mongo')
async def qpmc_approved_leave_list_mongo():

    db = client["QPMC_RasaChatbot"]
    collection = db["Approved_Leave"]
    a=collection.find()

    approved_leave_list = []

    for i in a:
        approved_leave_list.append(i['Leave Id'])
    return approved_leave_list


@app.get('/qpmc_rejected_leave_list_mongo')
async def qpmc_rejected_leave_list_mongo():

    db = client["QPMC_RasaChatbot"]
    collection = db["Rejected_Leave"]
    a=collection.find()

    rejected_leave_list=[]

    for i in a:
        rejected_leave_list.append(i['Leave Id'])
    return rejected_leave_list


@app.get('/qpmc_it_tickets')
async def qpmc_it_tickets():

    db = client["QPMC_RasaChatbot"]
    collection = db["ITTickets"]
    a=collection.find()

    it_tickets = []

    for i in a:
        print(i)
        it_tickets.append(i['Ticket ID'])
    return it_tickets

@app.get('/qpmc_it_tickets_insert')
async def qpmc_it_tickets_insert(tickettype:str,Hardwaretype:str,monitorsize : Union[str, None] = None):
    db = client["QPMC_RasaChatbot"]
    collection = db["ITTickets"]
    random_number = np.random.randint(10000, 100000)
    ticket_number = "TCKT"+str(random_number)
    print(ticket_number)
    if(Hardwaretype == "Monitor"):
        data = {
            "Ticket ID": ticket_number,
            "Ticket type": tickettype,
            "Hardware type": Hardwaretype,
            "Monitor Size": monitorsize
        }
    else:
        data = {
            "Ticket ID": ticket_number,
            "Ticket type": tickettype,
            "Hardware type": Hardwaretype
        }
    result = collection.insert_one(data)
    if result.inserted_id:
        print("ticket raised succesfully Inserted ID:", result.inserted_id)
        res= f"Leave Request ({ticket_number}) has been inserted"
    else:
        res= f"Leave Request ({ticket_number}) has not been inserted"
    return res

@app.get('/qpmc_it_tickets_details')
async def qpmc_it_tickets_details():

    db = client["QPMC_RasaChatbot"]
    collection = db["ITTickets"]
    a=collection.find()

    it_ticket_detail = []

    for i in a:
        ticket={}
        ticket["Ticket id"]=i['Ticket ID']
        ticket["Ticket type"]=i['Ticket type']
        ticket["Hardware type"]=i['Hardware type']
        if(i['Hardware type']=="monitor" or i['Hardware type']=="Monitor" ):
            ticket["Monitor Size"]=i['Monitor Size']
        it_ticket_detail.append(ticket)
    return it_ticket_detail






if __name__ == '__main__':
    uvicorn.run(app,port=8000, log_level="info")