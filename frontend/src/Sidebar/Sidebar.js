import React, { useState } from "react";
import {
    CDBSidebar,
    CDBSidebarContent,
    CDBSidebarHeader,
    CDBSidebarMenu,
    CDBSidebarMenuItem,
} from 'cdbreact';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {

    const [isOpen, setIsOpen] = useState(false);
    const toggleNavbar = () => {
        setIsOpen(!isOpen)
    }
    return (
        <>

            <div className="sidebar">
                <div style={{ height: '100vh', overflow: 'scroll initial' }}>
                    <CDBSidebar className={`${isOpen ? "shifted" : ""}`} textColor="#fff" backgroundColor="#333">

                        <CDBSidebarHeader prefix={<div
                            className="sidebar-btn-wrapper"
                            style={{
                                padding: '20px 5px',
                                fontSize: '25px',
                                fontWeight: '400',
                                textAlign: 'center'
                            }}
                        >
                            <img className="logo" src="https://qpmc.qa//ar/assets/images/seo/site-image.jpg" alt="react-logo" height={"60vh"} id="logo"
                            />

                        </div>} style={{ textAlign: 'center' }}>
                            <div className="qpmc">
                                <span>QPMC</span>
                            </div>


                        </CDBSidebarHeader>

                        <CDBSidebarContent className="sidebar-content">

                            <CDBSidebarMenu>
                                <NavLink exact to="/main-page/notification" activeClassName="activeClicked">
                                    <CDBSidebarMenuItem icon="file">Pending</CDBSidebarMenuItem>
                                </NavLink>
                                <NavLink exact to="/main-page/notification" activeClassName="activeClicked">
                                    <CDBSidebarMenuItem icon="download">Approved</CDBSidebarMenuItem>
                                </NavLink>
                                <NavLink exact to="/main-page/notification" activeClassName="activeClicked">
                                    <CDBSidebarMenuItem icon="ban">Rejected</CDBSidebarMenuItem>
                                </NavLink>
                                <NavLink exact to="/" activeClassName="activeClicked">
                                    <CDBSidebarMenuItem icon="home">Home</CDBSidebarMenuItem>
                                </NavLink>
                            </CDBSidebarMenu>
                        </CDBSidebarContent>
                        {/* <CDBSidebarFooter style={{ textAlign: 'center' }}>
                            <div
                                className="sidebar-btn-wrapper"
                                style={{
                                    padding: '20px 5px',
                                    fontSize: '22px',
                                    fontWeight: '400'
                                }}
                            >
                                QPMC
                                <img className="logo" src="https://qpmc.qa//ar/assets/images/seo/site-image.jpg" alt="react-logo" height={"50vh"} />
                            </div>
                        </CDBSidebarFooter> */}
                        <CDBSidebarHeader prefix={<i className="fa fa-bars fa-large" onClick={toggleNavbar}></i>}>
                            <a href="/" className="text-decoration-none" style={{ color: 'inherit' }}>
                                PORTAL
                            </a>
                        </CDBSidebarHeader>
                    </CDBSidebar>
                </div>
            </div>
        </>
    )
}

export default Sidebar;


/*

*/
