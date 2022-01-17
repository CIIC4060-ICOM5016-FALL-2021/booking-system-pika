import React, { useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Container, Form, Modal, ModalDescription, Segment} from "semantic-ui-react";
import axios from "axios";


// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function Schedule(){
    const [t,sett] = useState(false)
    const [r, setr] = useState(false);
    const [booking, setbooking] = useState(false);
    const [unavailable, setavailable] = useState(false);
    const [ba_id,setba_id] = useState("");
    const [st_dt, setst_dt] = useState("");
    const [et_dt, setet_dt] = useState("");
    const[room_id,setroom_id] = useState("");
    const[invitee,setinvitee]=  useState("");
    const[un,setun] =  useState("");
    const [updatebooking,setupdatebooking] = useState(false);
    const[deletebooking,setdeletebooking] =useState(false)
    const [deleteunavailable,setdeleteupunavailable]= useState(false);
    const [meetings,setmeetings] =useState([])
    let e = localStorage.getItem("login-data");
    let   dat = JSON.parse(e)
    const [info, setinfo] = useState(false);
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment)

    function getpersonschedule(){
        if (info==false) {
            axios.post('https://booking-system-pika.herokuapp.com/pika-booking/persons/person/all-schedule', {
                person_id: dat.p_id
            }).then(res => {
                let t = []
                let i =0
                for  (let meet of res.data.st_dt) {

                    const st =` ${res.data.st_dt[i]}-0400 (Atlantic Standard Time)`
                    const et = ` ${res.data.et_dt[i]}-0400 (Atlantic Standard Time)`
                    let tile =""
                    if ( res.data.bookingname[i]==""){
                        tile = "Unavailable"
                    }else{
                        tile = res.data.bookingname[i]
                    }

                const w = {title: tile, start:  new Date(st), end :  new Date(et), room: 4}
                t.push(w)
                    i=i+1
            }
                setmeetings(t)
        })
    }



    }


    const returnallfalse=()=>{
        setr(false)
        setOpen(false)
        setst_dt("")
        setet_dt("")
        setroom_id("")
        setinvitee("")

        setbooking(false)
        setavailable(false)
      setba_id("")
        setun("")
        setdeleteupunavailable(false)
        setupdatebooking(false)
        setr(false)
        setdeletebooking(false)
        setdeleteupunavailable(false)
        sett(false)
    }

    function getperson(){
        axios.post( "https://booking-system-pika.herokuapp.com/pika-booking/person/unavailable/id", {"Person_id": dat.p_id})
    }
    function check(){
        if (st_dt == "" || et_dt == "" || un==""){
            return true
        }else
        {
            return false
        }
    }

    return <>
        {getpersonschedule()}

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
