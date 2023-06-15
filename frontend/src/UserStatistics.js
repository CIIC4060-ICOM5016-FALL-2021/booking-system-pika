import React, {useEffect, useState} from 'react';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from "axios";
import {Link} from "react-router-dom";
function UserStatistics (){
    let [data,setdata] =  useState("");
    let [d,setd] =  useState("");
    let[name,setname] =  useState("");
    const [k,setk] =  useState(false);
    let e = localStorage.getItem("login-data");
    let   dat = JSON.parse(e)
    console.log(dat.p_id);
    function r() {
      if (k=== false){
            axios.get(
                `https://booking-system-pika.herokuapp.com//pika-booking/persons/${ dat.p_id}/most-booked-room`).then(res => {
                setdata(res.data);
                console.log(res.data)
            })
            axios.get(`https://booking-system-pika.herokuapp.com/pika-booking/persons/${dat.p_id}/shared`).then(res => {
                setd(res.data);
                console.log(d)




                    })

            axios.get(`https://booking-system-pika.herokuapp.com/pika-booking/persons/${d.p_id}`).then(res => {
                setname(res.data)
            })
        }
}
    function type1(parameter) {
        switch (parameter) {
            case 1:
                return 'laboratory'
            case 2:
                return 'classroom'
            case 3:
                return 'office'
            case 4:
                return 'study_space'
            case 5:
                return 'conference_hall'
        }
    }
    useEffect(()=>{
        r()
        setk(true)
    })
        return <>

                <h1>  Most Used Room By You:
             <h1> RoomName: {data.r_name} ,Building: {data.r_building} ,  Dept: {data.r_dept}  , Type: {type1(data.r_type)}  </h1>
                </h1>
            <h1>User most booked with You:    {name.p_fname} {name.p_lname}</h1>
                        <Link to = "/Dashboard" > <button>
                Go to Dashboard
            </button>
            </Link>

        </>

}

export default UserStatistics;