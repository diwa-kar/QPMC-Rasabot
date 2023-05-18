import React, { useEffect, useState } from "react";
import ApprovalModal from "../modals/ApprovalModal";
import EmptyIcon from "./empty.png";
import NotificationItem from "./NotificationItem";
import "./NotificationDisplay.css";
import axios from "axios";
import { toast } from "react-toastify";
import PuffLoader from "react-spinners/PuffLoader";
import Button from "@mui/material/Button";

const Notificationdisplay = ({
  selectedItem,
  isSidebarOpen,
  tab,
  cards,
  setCards,
  displayShow,
  setDisplayShow,
}) => {
  const [modalShow, setModalShow] = React.useState(false);
  const [status, setStatus] = React.useState("");
  const [loader, setLoader] = useState(true);
  const [detailData, setDetailData] = useState([
    // {
    //   "Purchase Requisition Number": "1000005421",
    //   "Purchase Requisition Item Number": "10",
    //   "Purchase Requisition Release Status": "05",
    //   Purchase_Requisition_Item_Text: "TEST KIROA 005",
    //   Purchase_Requisition_Material_Group: "20001",
    //   Requested_Quantity: "2.000",
    //   Base_Unit: "PC",
    //   Purchase_Requisition_Price: "2543.84",
    //   Plant: "2000",
    //   Company_Code: "2000",
    //   Processing_Status: "N",
    //   Delivery_Date: "2022-07-01T00:00:00",
    //   Creation_Date: "2022-06-30T00:00:00",
    // },
  ]);

  const getDetails = async () => {
    setDisplayShow(true);
    setDetailData([]);
    setLoader(true);
    let uri = "";
    // selectedItem.type &&
    // selectedItem.type == "Pending Request"
    if (selectedItem) uri = "qmpc_pending_pr_item_info";
    if (uri != "") {
      try {
        axios
          .get(
            `http://localhost:8000/${uri}?prno=${
              selectedItem.value.split(" ")[1]
            }`
          )
          .then((response) => {
            const data = response.data;
            const tempData = [];
            Object.keys(data).map((key, index) => {
              tempData.push(data[key]);
            });
            setLoader(false);
            setDisplayShow(true);
            setDetailData(tempData);
          })
          .catch((error) => console.log(`Error in Axios ${error}`));
      } catch (e) {
        console.log(e);
      }
    } else {
      console.log();
    }
  };
  useEffect(() => {
    getDetails();
  }, [selectedItem]);

  useEffect(() => {
    setDetailData([]);
  }, [tab]);

  function approveRequest() {
    try {
      axios
        .get(
          `http://localhost:8000/qpmc_pending_pr_approval?prno=${
            selectedItem.value.split(" ")[1]
          }`
        )
        .then((response) => {
          const data = response.data;
          console.log(data);
          if (data.result.ExStatus == "ERROR") toast.error(data.text);
          if (data.result.ExStatus == "APPROVED") toast.success(data.text);
          setCards(cards.filter((card) => card.value != selectedItem.value));
          setDetailData([]);
        })
        .catch((error) => console.log(`Error in Axios ${error}`));
    } catch (e) {
      console.log(e);
    }
  }

  function rejectRequest() {
    try {
      axios
        .get(
          `http://localhost:8000/qpmc_pending_pr_reject?prno=${
            selectedItem.value.split(" ")[1]
          }`
        )
        .then((response) => {
          const data = response.data;
          console.log(data);
          if (data.result.ExStatus == "ERROR") toast.error(data.text);
          if (data.result.ExStatus == "REJECTED") toast.warning(data.text);
          setCards(cards.filter((card) => card.value != selectedItem.value));
          setDetailData([]);
        })
        .catch((error) => console.log(`Error in Axios ${error}`));
    } catch (e) {
      console.log(e);
    }
  }

  return (
    <div
      className="Notificataion-display"
      style={{
        width: "69%",
      }}
    >
      {detailData.length > 0 ? (
        <div className="Notificataion-display-title">
          <span>{tab} Notification</span>
        </div>
      ) : (
        <></>
      )}

      {detailData.length > 0 && tab == "Pending" ? (
        <div className="Notificataion-display-buttons">
          <Button
            variant={"contained"}
            size="medium"
            sx={{
              backgroundColor: "#1b5e20",
              fontWeight: "bold",
            }}
            style={{
              margin: "5px 0px",
              textTransform: "capitalize",
              letterSpacing: "1px",
              fontSize: "11px",
              fontWeight: "550",
              width: "12%",
              fontWeight: "700",
              marginRight: "20px",
            }}
            color="success"
            onClick={() => approveRequest()}
          >
            Approve
          </Button>
          <Button
            variant={"contained"}
            size="medium"
            sx={{
              backgroundColor: "#c62828",
            }}
            style={{
              margin: "5px 0px",
              textTransform: "capitalize",
              letterSpacing: "1px",
              fontSize: "11px",
              fontWeight: "550",
              width: "12%",
              fontWeight: "700",
            }}
            color="error"
            onClick={() => rejectRequest()}
          >
            Reject
          </Button>
        </div>
      ) : (
        <></>
      )}
      {detailData.length > 0 ? (
        <div className="Notificataion-display-content">
          {detailData.map((data, index) => {
            return (
              <div
                className="Notificataion-display-detail"
                key={index}
                style={{
                  background: tab=='Pending' ? "#fffdf6": tab=='Approved'?"#f3fffc":"#fff7f7",
                  boxShadow: "rgba(0, 0, 0, 0.24) 0px 3px 8px"
                  // marginBottom: detailData.length == index + 1 ? "20px" : "0px",
                }}
              >
                {Object.keys(data).map((key, keyIndex) => (
                  <div>
                    <span
                      style={{
                        color: "#820000",
                        wordWrap: "break-word",
                      }}
                    >
                      {key}
                    </span>
                    <span
                      style={{
                        margin: "0px 4px",
                        color: "darkblue",
                      }}
                    >
                      :
                    </span>
                    <span
                      style={{
                        color: "black",
                      }}
                    >
                      {data[key]}
                    </span>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      ) : (
        <></>
      )}
      {detailData.length == 0 && displayShow == false ? (
        <div
          style={{
            width: "100%",
            height: "80%",
            display: "flex",
            alignItems: "center",
            flexDirection: "column",
            justifyContent: "center",
            opacity: "0.7",
          }}
        >
          <img
            src={EmptyIcon}
            style={{
              width: "20%",
              marginTop: "100px",
            }}
          />
          <span
            style={{
              color: "grey",
              fontSize: "15px",
              letterSpacing: "0.5px",
              textAlign: "center",
              marginTop: "50px",
            }}
          >
            Choose PR Number to view line item description...
          </span>
        </div>
      ) : (
        <></>
      )}
      <div
        style={{
          height: "90%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <PuffLoader
          color="#936C29"
          loading={loader}
          size={100}
          aria-label="Loading Spinner"
          data-testid="loader"
        />
      </div>
    </div>
  );
};

export default Notificationdisplay;
