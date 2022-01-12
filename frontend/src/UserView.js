import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Tab} from "semantic-ui-react";
import BookMeeting from "./BookMeeting";
import Schedule from "./Schedule";
import UserStatistics from "./UserStatistics";
import Settings from "./Settings";
import RoomManagement from "./RoomManagement";
function UserView(){
    const [isAuth, setIsAuth] = useState(false)
    const panes = [

        {
            menuItem: 'Booking', render: () => <BookMeeting/>
        },
        {
            menuItem: 'Schedule', render: () => <Schedule/>
        },
        {
            menuItem: 'UserStatistics', render: () => <UserStatistics/>
        },
        {
            menuItem: 'Room Management', render: () => < RoomManagement/>
        },
        {
            menuItem: 'Account', render: () => <Settings/>
        }
    ]

    return <Tab panes={panes}/>

}
export default UserView;
