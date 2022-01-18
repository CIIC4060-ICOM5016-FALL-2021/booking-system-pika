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
            axios.post('https://booking-system-pika.herokuapp.com/pika-booking/persons/person/all-schedule', {
                person_id: dat.p_id
            }).then(res => {
                let t = []
                let i =0
                for  (let meet of res.data.st_dt) {

                    const st =` ${res.data.st_dt[i]}-0400 (Atlantic Standard Time)`
                    const et = ` ${res.data.et_dt[i]}-0400 (Atlantic Standard Time)`
                    let tile =""
                  //  if ( res.data.booking_name[i]===""){
                        tile = "Unavailable"
                  //  }else{
                  //     tile = res.data.booking_name[i]
                  //  }

                const w = {title: tile, start:  new Date(st), end :  new Date(et), room: 4}
                t.push(w)
                    i=i+1
            }
                setmeetings(t)
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
