import React, {Component, useState} from 'react';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios, {Axios} from "axios";
import {Link, Route} from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";
function UserStatistics (){
    let [data,setdata] =  useState("");
    let [d,setd] =  useState("");
    let[name,setname] =  useState("");
    let e = localStorage.getItem("login-data");
    let   dat = JSON.parse(e)
    console.log(dat.p_id);
        axios.post('https://booking-system-pika.herokuapp.com/pika-booking/persons/person/most-booked-room', {"p_id": data.p_id}).then(res => {
            setdata(res.data);

        })
        axios.post('https://booking-system-pika.herokuapp.com/pika-booking/persons/shared',{"p_id": data.p_id}).then(res => {
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