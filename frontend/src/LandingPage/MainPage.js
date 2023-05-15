import React, { useEffect, useState } from "react";
import "../App.css";
import Sidebar from "../Sidebar/Sidebar";
import MiddleNavbar from "../NotificationSidebar/MiddleNavbar";
import { Link, Outlet } from "react-router-dom";
import Notificationdisplay from "../NotificationSidebar/Notificationdisplay";
import NotificationItem from "../NotificationSidebar/NotificationItem";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function MainPage(props) {
  const [selectedItem, setSelectedItem] = useState([]);
  const [activeTab, setActiveTab] = useState("Pending");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [displayShow, setDisplayShow] = useState(false);
  const [cards, setCards] = useState([
    // {
    //   type: "Pending Request",
    //   value: "PR 1000005421",
    // },
    // {
    //   type: "Pending Request",
    //   value: "PR 1000005447",
    // },
    // {
    //   type: "Pending Request",
    //   value: "PR 1000005455",
    // },
    // {
    //   type: "Pending Request",
    //   value: "PR 1000005456",
    // },
    // {
    //   type: "Pending Request",
    //   value: "PR 1000005496",
    // },
  ]);
  useEffect(() => {
    setCards([]);
    setDisplayShow(false);
  }, [activeTab]);
  return (
    <div className="App">
      <ToastContainer
        autoClose={2000}
        hideProgressBar={true}
        newestOnTop={true}
        closeOnClick
      />
      <Sidebar
        setTab={(value) => setActiveTab(value)}
        tab={activeTab}
        setIsOpen={(value) => setSidebarOpen(value)}
        isOpen={sidebarOpen}
      />

      <MiddleNavbar
        updateValues={(value) => setSelectedItem(value)}
        activeTab={activeTab}
        setCards={setCards}
        cards={cards}
      />
      <Notificationdisplay
        selectedItem={selectedItem}
        isSidebarOpen={sidebarOpen}
        tab={activeTab}
        setCards={setCards}
        cards={cards}
        displayShow={displayShow}
        setDisplayShow={setDisplayShow}
      />
    </div>
  );
}

export default MainPage;

{
  /* <div className="App">
      <div className="row gx-0">
        <div className="col-md-5 gy-0">
          <div className="leftside d-flex">
            <div className="flex-box">
              <Sidebar
                setTab={(value) => setActiveTab(value)}
                tab={activeTab}
              />
              <MiddleNavbar
                updateValues={(value) => setSelectedItem(value)}
                activeTab={activeTab}
              ></MiddleNavbar>
            </div>
          </div>
        </div>

        <div className="col-md-7 gy-0">
          <div className="rightside d-flex judtify-contents-center text-align-center">
            <Notificationdisplay selectedItem={selectedItem} />
          </div>
        </div>
      </div>
    </div> */
}
