import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import axios, {Axios} from "axios";
import {Button,
    Divider,
    Grid,
    Header,
    Icon,
    Search,
    Segment,
    Dimmer,
    Loader,
    Label,
    Input
} from 'semantic-ui-react'
import {Link, Route} from "react-router-dom";
import bookMeeting from "./BookMeeting";
import Navbar from "./components/Navbar/Navbar";
import UserView from "./UserView";
function UserStatistics (){
    let [data,setdata] =  useState("");
    let [d,setd] =  useState("");


        axios.post('https://booking-system-pika.herokuapp.com/pika-booking/persons/person/most-booked-room', {"p_id": '5'}).then(res => {
            setdata(res.data);

        })
        axios.post('https://booking-system-pika.herokuapp.com/pika-booking/persons/shared',{"p_id": '5'}).then(res => {
            setd(res.data);
        })



        return <>
                <h1>  Most Used Room By You:
                    {data.r_building}
                </h1>
            <h1>User most booked with You:    {d.p_id}</h1>
                        <Link to = "/Dashboard" > <button>
                Go to Dashboard
            </button>
            </Link>
            <Link to = "/rooms" > <button>
                Go to room list
            </button>
            </Link>
            <Link to = "/person" > <button>
                Go to Person list
            </button>
            </Link>
        </>

}

export default UserStatistics;