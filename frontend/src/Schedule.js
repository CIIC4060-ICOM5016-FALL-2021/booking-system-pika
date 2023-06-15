import React, {useEffect, useState} from 'react';
import {Calendar, momentLocalizer } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import { Container} from "semantic-ui-react";
import axios from "axios";


// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function Schedule(){

    const [meetings,setmeetings] =useState([])
    let e = localStorage.getItem("login-data");
    let   dat = JSON.parse(e)
    const localizer = momentLocalizer(moment)

    function getpersonschedule(){
            axios.get(`https://booking-system-pika.herokuapp.com/pika-booking/persons/person/all-schedule/${dat.p_id}`
            ).then(res => {
                let t = []

                for  (let meet of res.data) {

                    const st =` ${meet.st_dt}-0400 (Atlantic Standard Time)`
                    const et = ` ${meet.et_dt}-0400 (Atlantic Standard Time)`
                    let tile =""
                   if ( meet.name===null||meet.name==='unavailable'){
                       tile = "Unavailable"
                       const w = {title: `${tile}`, start: new Date(st), end: new Date(et)}
                       t.push(w)
                   }else{
                       tile = ` ${meet.name}`
                       const w = {title: `${tile}___________room: ${meet.room_name}`, start: new Date(st), end: new Date(et)}
                       t.push(w)
                                        }




            }
                setmeetings(t)
                console.log(meetings)
        })




    }



    useEffect(()=>{
        getpersonschedule()
    })

    return <>

    <Container style={{ height: 800 }}><Calendar
        localizer={localizer}
        startAccessor="start"
        events={meetings}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
    >

    </Calendar>

    </Container>


</>

}
export default Schedule;
