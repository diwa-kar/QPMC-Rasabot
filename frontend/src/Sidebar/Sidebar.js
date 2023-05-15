import React, { useState } from "react";
import QPMCLogo from "./qpmc-logo.png";
import {
  CDBSidebar,
  CDBSidebarContent,
  CDBSidebarHeader,
  CDBSidebarMenu,
  CDBSidebarMenuItem,
} from "cdbreact";
import { NavLink } from "react-router-dom";

const Sidebar = ({ setTab, tab, setIsOpen, isOpen }) => {
  const toggleNavbar = () => {
    setIsOpen(!isOpen);
  };
  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <img src={QPMCLogo} alt="Logo" />
      </div>
      <div className="sidebar-content">
        <div
          className="sidebar-items"
          style={{
            color: tab == "Home" ? "#820000" : "#000",
          }}
          onClick={() => setTab("Home")}
        >
          <i class="fa-solid fa-house"></i>
          <span>HOME</span>
        </div>
        <div
          className="sidebar-items"
          style={{
            color: tab == "Pending" ? "#820000" : "#000",
          }}
          onClick={() => setTab("Pending")}
        >
          <i class="fa-solid fa-circle-stop"></i>
          <span>PENDING PR</span>
        </div>
        <div
          className="sidebar-items"
          style={{
            color: tab == "Approved" ? "#820000" : "#000",
          }}
          onClick={() => setTab("Approved")}
        >
          <i class="fa-solid fa-check-to-slot"></i>
          <span>APPROVED PR</span>
        </div>
        <div
          className="sidebar-items"
          style={{
            color: tab == "Rejected" ? "#820000" : "#000",
          }}
          onClick={() => setTab("Rejected")}
        >
          <i class="fa-solid fa-rectangle-xmark"></i>
          {/* <svg
            fill={tab == "Rejected" ? "#820000" : "#000"}
            width="80%"
            height="60%"
            viewBox="0 0 64 64"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            xmlnsXlink="http://www.w3.org/1999/xlink"
            xmlSpace="preserve"
            xmlnsSerif="http://www.serif.com/"
            style={{
              fillRule: "evenodd",
              clipRule: "evenodd",
              strokeLinejoin: "round",
              strokeMiterlimit: 2,
            }}
          >
            <rect
              id="Icons"
              x="-256"
              y="-256"
              width="1280"
              height="800"
              style={{ fill: "none" }}
            />

            <g id="Icons1" serifId="Icons">
              <g id="Strike"></g>

              <g id="H1"></g>

              <g id="H2"></g>

              <g id="H3"></g>

              <g id="list-ul"></g>

              <g id="hamburger-1"></g>

              <g id="hamburger-2"></g>

              <g id="list-ol"></g>

              <g id="list-task"></g>

              <g id="trash"></g>

              <g id="vertical-menu"></g>

              <g id="horizontal-menu"></g>

              <g id="sidebar-2"></g>

              <g id="Pen"></g>

              <g id="Pen1" serifId="Pen"></g>

              <g id="clock"></g>

              <g id="external-link"></g>

              <g id="hr"></g>

              <g id="info"></g>

              <g id="warning"></g>

              <g id="plus-circle"></g>

              <path
                id="denied"
                d="M32.266,7.951c13.246,0 24,10.754 24,24c0,13.246 -10.754,24 -24,24c-13.246,0 -24,-10.754 -24,-24c0,-13.246 10.754,-24 24,-24Zm-15.616,11.465c-2.759,3.433 -4.411,7.792 -4.411,12.535c0,11.053 8.974,20.027 20.027,20.027c4.743,0 9.102,-1.652 12.534,-4.411l-28.15,-28.151Zm31.048,25.295c2.87,-3.466 4.596,-7.913 4.596,-12.76c0,-11.054 -8.974,-20.028 -20.028,-20.028c-4.847,0 -9.294,1.726 -12.76,4.596l28.192,28.192Z"
              />

              <g id="minus-circle"></g>

              <g id="vue"></g>

              <g id="cog"></g>

              <g id="logo"></g>

              <g id="radio-check"></g>

              <g id="eye-slash"></g>

              <g id="eye"></g>

              <g id="toggle-off"></g>

              <g id="shredder"></g>

              <g
                id="spinner--loading--dots-"
                serifId="spinner [loading, dots]"
              ></g>

              <g id="react"></g>

              <g id="check-selected"></g>

              <g id="turn-off"></g>

              <g id="code-block"></g>

              <g id="user"></g>

              <g id="coffee-bean"></g>

              <g id="coffee-beans">
                <g id="coffee-bean1" serifId="coffee-bean"></g>
              </g>

              <g id="coffee-bean-filled"></g>

              <g id="coffee-beans-filled">
                <g id="coffee-bean2" serifId="coffee-bean"></g>
              </g>

              <g id="clipboard"></g>

              <g id="clipboard-paste"></g>

              <g id="clipboard-copy"></g>

              <g id="Layer1"></g>
            </g>
          </svg> */}
          <span>REJECTED PR</span>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;

/*

*/
