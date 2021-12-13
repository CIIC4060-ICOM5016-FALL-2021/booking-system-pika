import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import axios, {Axios} from "axios";
import {data}  from "/"
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
function UserStatistics (){
    let [data,setdata] =  useState("");
    let [d,setd] =  useState("");
    let[name,setname] =  useState("");
const login = localStorage.getItem('Login')
        axios.post('https://booking-system-pika.herokuapp.com/pika-booking/persons/person/most-booked-room', {"p_id": login}).then(res => {
            setdata(res.data);

        })
        axios.post('https://booking-system-pika.herokuapp.com/pika-booking/persons/shared',{"p_id": '5'}).then(res => {
            setd(res.data);
        })

       axios.post('https://booking-system-pika.herokuapp.com/pika-booking/persons/id',{"p_id": d.p_id}).then(res =>{
           setname(res.data)
       })

        return <>
            <Navbar/>
                <h1>  Most Used Room By You:
             <h1>  Building: {data.r_building} ,  Dept: {data.r_dept}  , Type: {data.r_type}  </h1>
                </h1>
            <h1>User most booked with You:    {name.p_fname} {name.p_lname}</h1>
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