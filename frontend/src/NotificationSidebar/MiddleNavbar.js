import React, { useEffect, useState } from "react";
import NotificationItem from "./NotificationItem";
import PuffLoader from "react-spinners/PuffLoader";
import { Form } from "reactstrap";
import { values } from "lodash";

const MiddleNavbar = (props) => {
  const [iconState, setIconState] = useState("fa fa-search");

  const [isSearchMode, setIsSearchMode] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");

  const makeAPICall = async () => {
    let uri = "";
    let uri1 = "";
    let uri2= "";
    let pending_prlist=[];
    let pending_leave=[];
    let approved_prlist=[];
    let approved_leave=[];
    let rejected_prlist=[];
    let rejected_leave=[];
    let it_tickets=[];
    if (props.activeTab == "Pending") {
      uri = "qpmc_pending_pr";
      uri1 = "qpmc_leave_reuqest_sf";
      uri2 = "qpmc_it_tickets"
      try {
        const response = await fetch(`http://localhost:8000/${uri}`, {
          mode: "cors",
        });
        const data = await response.json();
        console.log(data);
        let type = "pending pr";
        if (data && data.pending_pr) {
          pending_prlist= 
            data.pending_pr.map((data, index) => ({
              type: type,
              value: data,
            }))
        }
        const response1 = await fetch(`http://localhost:8000/${uri1}`, {
          mode: "cors",
        });
        const data1 = await response1.json();
        console.log(data1);
        let type1 = "pending leave";
        if (data1) {
          pending_leave = 
            data1.map((data, index) => {
              let some = 0;
              for (const [key, value] of Object.entries(data)) {
                if (key === "Leave Id") {
                  some = value;
                }
              }
              return {
                type: type1,
                value: some,
              };
            })
        }
        const response2 = await fetch(`http://localhost:8000/${uri2}`, {
          mode: "cors",
        });
        const data2 = await response2.json();
        console.log(data);
        let type2 = "it ticket";
        if (data2) {
          it_tickets= 
            data2.map((item, index) => ({
              type: type2,
              value: item
            }))
        }
        // console.log(it_tickets);
        // console.log(it_tickets.concat(pending_prlist.concat(pending_leave)))
        props.setCards(it_tickets.concat(pending_prlist.concat(pending_leave)))
      } catch (e) {
        console.log(e);
      }
    }else if (props.activeTab == "Approved") {
      uri = "qpmc_approved_pr_list_mongo";
      uri1 = "qpmc_approved_leave_list_mongo";
      try {
        const response = await fetch(`http://localhost:8000/${uri}`, {
          mode: "cors",
        });
        const data = await response.json();
        console.log(data);
        let type = "approved pr";
        if (data) {
          approved_prlist= 
            data.map((item, index) => ({
              type: type,
              value: item
            }))
        }
        const response1 = await fetch(`http://localhost:8000/${uri1}`, {
          mode: "cors",
        });
        const data1 = await response1.json();
        console.log(data1);
        let type1 = "approved leave";
        if (data1) {
          approved_leave =
          data1.map((item, index) => ({
            type: type1,
            value: item
          }))
        }
        console.log(approved_prlist.concat(approved_leave))
        props.setCards(approved_leave.concat(approved_prlist))
      } catch (e) {
        console.log(e);
      }
    };

    if (props.activeTab === "Rejected") {
      uri = "qpmc_rejected_pr_list_mongo"
      uri1 = "qpmc_rejected_leave_list_mongo"
      try {
        const response = await fetch(`http://localhost:8000/${uri}`, {
          mode: "cors",
        });
        const data = await response.json();
        console.log(data);
        let type = "rejected pr";
        if (data) {
          rejected_prlist= 
            data.map((item, index) => ({
              type: type,
              value: item
            }))
        }
        const response1 = await fetch(`http://localhost:8000/${uri1}`, {
          mode: "cors",
        });
        const data1 = await response1.json();
        console.log(data1);
        let type1 = "rejected leave";
        if (data1) {
          rejected_leave =
          data1.map((item, index) => ({
            type: type1,
            value: item
          }))
        }
        console.log(approved_prlist.concat(approved_leave))
        props.setCards(rejected_leave.concat(rejected_prlist))
      } catch (e) {
        console.log(e);
      }
    };

    
    // if (props.activeTab == "Pending") uri = "qpmc_pending_pr";
    // if (props.activeTab == "Approved") uri = "qpmc_approved_pr_list_mongo";
    // if (props.activeTab == "Rejected") uri = "qpmc_rejected_pr_list_mongo";
    // if (uri != "") {
    //   try {
    //     const response = await fetch(`http://localhost:8000/${uri}`, {
    //       mode: "cors",
    //     });
    //     const data = await response.json();
    //     let type = "";
        // if (props.activeTab == "Pending") {
        //   type = "Pending Request";
        //   if (data && data.pending_pr) {
        //     props.setCards(
        //       data.pending_pr.map((data, index) => ({
        //         type: type,
        //         value: data,
        //       }))
        //     );
        //   }
        // }
        // if (props.activeTab == "Approved") {
        //   props.setCards(
        //     data.map((item, index) => ({
        //       value: item,
        //     }))
        //   );
        // }
        // if (props.activeTab == "Rejected") {
        //   props.setCards(
        //     data.map((item, index) => ({
        //       value: item,
        //     }))
        //   );
        // }
        // if (data && data.pending_pr) {
        //   props.setCards(
        //     data.pending_pr.map((data, index) => ({
        //       type: "Pending Request",
        //       value: data,
        //     }))
        //   );
        // }
    //   } catch (e) {
    //     console.log(e);
    //   }
    // } else {
    //   // props.setCards([]);
    // }
  };
  useEffect(() => {
    makeAPICall();
  }, [props.activeTab]);

  const handleClick = () => {
    setIsSearchMode(true);
    console.log(props);
  };

  function removeCard() {}

  const handleInputChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleItem = () => {
    console.log("Button clicked!");
    console.log(props);
  };
  const setUpdateIt = (values) => {
    props.updateValues(props.cards[values]);
  };

  return (
    <div className="middle-sidebar">
      <div
        style={{
          width: "100%",
          height: "100%",
        }}
      >
        {/* Your code goes here */}
        <div
          style={{
            width: "100%",
            height: "100%",
            listStyle: "none",
            padding: 0,
            boxShadow:
              "rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px",
          }}
        >
          {isSearchMode ? (
            <Form className="nosubmit">
              <input
                className="nosubmit mr-sm-2 search-box"
                type="text"
                placeholder="Search..."
                value={searchTerm}
                onChange={handleInputChange}
              />
            </Form>
          ) : (
            <span className="Notification" onClick={handleClick}>
              Notifications
              {/* <i
                className={iconState}
                aria-hidden="true"
                style={{ marginLeft: "3.9vw" }}
              ></i> */}
            </span>
          )}
          {props.cards.length == 0 ? (
            <div
              style={{
                height: "75%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <PuffLoader
                color="#936C29"
                loading={true}
                size={100}
                aria-label="Loading Spinner"
                data-testid="loader"
              />
            </div>
          ) : (
            <NotificationItem
              cardItems={props.cards}
              updateIt={props.updateValues}
              // leaveDetail={props.leaveItem}
              tab={props.activeTab}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default MiddleNavbar;
