import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const NotificationItem = (props) => {
  const navigate = useNavigate();

  const handleItemClick = (index) => {
    console.log("handleItemClick clicked inside notification item");
    console.log(props.purchaseRequisitions[index]);
    props.updateIt(props.purchaseRequisitions[index]);
  };
  return (
    <div>
      <ul>
        {props.purchaseRequisitions.map((pr, index) => (
          <li
            key={index}
            onClick={() => handleItemClick(index)}
            style={{
              width: "100%",
              height: "100px",
              borderBottom: "1px solid #ccc",
              display: "flex",
              alignItems: "center",
              paddingLeft: "10px",
            }}
          >
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                fontSize: "17px",
              }}
            >
              <span style={{ fontWeight: "bold" }}>
                Purchase Requisition Number: {pr.purchaseRequisition}
              </span>
              <span>{pr.purchaseRequisitionType}</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default NotificationItem;
