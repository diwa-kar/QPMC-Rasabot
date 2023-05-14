import React, { useState } from "react";
import "../App.css";
import Sidebar from "../Sidebar/Sidebar";
import MiddleNavbar from "../NotificationSidebar/MiddleNavbar";
import { Link, Outlet } from "react-router-dom";
import Notificationdisplay from "../NotificationSidebar/Notificationdisplay";
import NotificationItem from "../NotificationSidebar/NotificationItem";

function MainPage(props) {
  const [selectedItem, setSelectedItem] = useState([]);

  function setDisplayState(value) {
    setSelectedItem(value);
    console.log("in display state", value);
  }

  return (
    <div className="App">
      <div className="row gx-0">
        <div className="col-md-5 gy-0">
          <div className="leftside d-flex">
            <div className="flex-box">
              <Sidebar />
              <MiddleNavbar updateValues={setDisplayState}></MiddleNavbar>
            </div>
          </div>
        </div>

        <div className="col-md-7 gy-0">
          <div className="rightside d-flex judtify-contents-center text-align-center">
            {/* <div className='nav-flex-box'> */}
            {/* <div className='main-panel'> */}
            {/* <Link to="/main-page/notification"></Link>
            <Outlet /> */}
            <Notificationdisplay selectedItem={selectedItem} />
            {/* </div> */}
          </div>
        </div>
      </div>
    </div>
  );
}

export default MainPage;
