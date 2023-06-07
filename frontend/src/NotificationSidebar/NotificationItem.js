import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const NotificationItem = (props) => {
  const navigate = useNavigate();
  useEffect(()=>{
    console.log(props.cardItems)
  },[])

  const handleItemClick = (index, card) => {
    if (card.type == "pending pr") {
      props.updateIt(props.cardItems[index]);
    }else if (card.type == "pending leave") {
      // console.log(card);
      props.updateIt(card);
    }else if (card.type == "it ticket") {
      // console.log(card);
      props.updateIt(card);
    }
  };
  return (
    <div
      style={{
        margin: "0px 5px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "flex-start",
        height: "100%",
        overflowY: "scroll",
      }}
      className="NotificationItem"
    >
      {props.cardItems &&
        props.cardItems.map((card, index) => (
          <div
            key={index}
            onClick={() => handleItemClick(index, card)}
            style={{
              width: "90%",
              height: "100px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-evenly",
              borderRadius: "6px",
              alignItems: "flex-start",
              background: "white",
              boxShadow: "rgba(0, 0, 0, 0.24) 0px 3px 8px",
              margin: "8px 0px",
              padding: "8px 0px",
              paddingLeft: "10px",
              borderTopLeftRadius: "0px",
              borderBottomLeftRadius: "0px",
              borderLeft: `4px solid ${
                props.tab == "Pending"
                  ? card.type == "pending leave"
                    ? "#7CB9E8"
                    : card.type == "pending pr" ?"goldenrod" : "#FFFD9E" 
                  : props.tab == "Approved"
                  ? "#00ab00"
                  : "#da2323"
              }`,
              cursor: "pointer",
            }}
          >
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                fontSize: "15px",
                width: "100%",
                margin: "10px 0px",
              }}
            >
              {card.type === "pending leave"? <span style={{ fontWeight: "bold" }}>{"PL "}{card.value}</span> 
              : <span style={{ fontWeight: "bold" }}>{card.value}</span>}
            </div>
            {card.type ? (
              <span
                style={{
                  textAlign: "left",
                  width: "fit-content",
                  padding: "1px 4px",
                  letterSpacing: "0.5px",
                  color: "white",
                  fontWeight: "bold",
                  fontSize: "6px",
                  background:
                    card.type === "pending leave" ? "#002D62" : card.type === "pending pr" ? "#820000" 
                    : card.type === "approved leave" || card.type === "approved pr" ? "#00ab00" 
                    : card.type === "rejected leave" || card.type === "rejected pr" ? "#da2323"
                    : card.type === "it ticket" ? "#7D7B00": "#7D7B00",
                  borderRadius: "2px",
                  textTransform: "uppercase",
                }}
              >
                {card.type}
              </span>
            ) : (
              <></>
            )}
          </div>
        ))}
    </div>
  );
};

export default NotificationItem;
