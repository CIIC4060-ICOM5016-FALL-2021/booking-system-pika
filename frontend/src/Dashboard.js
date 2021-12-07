import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal} from "semantic-ui-react";
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import Dashboard from "./Dashboard";
import Navbar from "./components/Navbar/Navbar";
import Rooms from "./components/Rooms";
function BookMeeting(){


    return <>
        <Navbar/>

        <h1> Most Booked Person:  <GetMostBookedPerson/> </h1>
        <h1> Most Booked Room: </h1>
        <h1>Busiest Hours:</h1>
        <button> Back to home menu </button>
        <Rooms/>
    </>
}
function GetMostBookedPerson(){
    return 1
}
function GetMostBookedRoom(){
    return 2
}
function GetBusiestHours(){
    return 3
}

export default BookMeeting;
