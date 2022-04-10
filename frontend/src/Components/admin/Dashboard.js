import React from "react";
import AdminProvider from "../../tools/useAdmin";
import {Outlet} from "react-router-dom";

export default function Dashboard() {
    return (
        <AdminProvider>
            <Outlet/>
        </AdminProvider>
    )
}