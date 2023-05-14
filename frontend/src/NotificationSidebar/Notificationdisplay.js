import React from "react";
import ApprovalModal from "../modals/ApprovalModal";
import NotificationItem from "./NotificationItem";
import { useLocation } from "react-router-dom";

const Notificationdisplay = ({ selectedItem }) => {
    const location = useLocation();
    // const purchaseRequisition = location.state?.purchaseRequisition;
    // const purchaseRequisitionType = location.state?.purchaseRequisitionType;

    const [modalShow, setModalShow] = React.useState(false);
    const [status, setStatus] = React.useState('');

    return (
        <>
            <div className="container">
                <div className="title-box">Purchase Requisition Number: <br />
                    {selectedItem?.purchaseRequisition}
                </div>
                <div className="body-box">
                    Purchase Requisition Type:  {selectedItem?.purchaseRequisitionType}<br />
                    Source Determination: {selectedItem?.SourceDetermination}<br/>
                    Last Updated At: {selectedItem?.date}
                </div>
                <div className="btn-box">
                    <button className="btn btn-success" onClick={() => { setModalShow(true); setStatus('Approve'); }}>Approve</button>
                    <button className="btn btn-danger" onClick={() => { setModalShow(true); setStatus('Reject'); }}>Reject</button>
                    <ApprovalModal status={status} show={modalShow} onHide={() => { setModalShow(false) }} />
                </div>
                <div></div>
                <div></div>
            </div>
        </>
    )
}

export default Notificationdisplay;