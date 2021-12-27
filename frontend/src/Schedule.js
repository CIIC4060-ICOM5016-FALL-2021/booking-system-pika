import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Segment} from "semantic-ui-react";
import {Link} from "react-router-dom";
import axios from "axios";


// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function Schedule(){
    const [t,sett] = useState("")
    const [r, setr] = useState(false);
    const [booking, setbooking] = useState(false);
    const [unavailable, setavailable] = useState(false);
    const [mark,setmark] = useState(false);
    const [st_dt, setst_dt] = useState("");
    const [et_dt, setet_dt] = useState("");
    const[room_id,setroom_id] = useState("");
    const[invitee,setinvitee]=  useState("");
    const [g,setg]= useState(false);
    const [dates, setDates] = useState([{
        'title': 'Selection',
        'allDay': false,
        'start': new Date(moment.now()),
        'end': new Date(moment.now())
    }]);
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment)
    axios.post(' https://booking-system-pika.herokuapp.com/pika-booking/persons/available/timeframe',{"pid": 5,"date": dates}).then(res=>{

    })
    return <>
    <Container style={{ height: 800 }}><Calendar
        localizer={localizer}
        startAccessor="start"
        events={dates}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
    >

    </Calendar>
        <Modal open={booking}
               onClose={() => setbooking(false)}
               onOpen={() => setbooking(true)}>
            <Modal.Header>What do you want to change of your booking?</Modal.Header>
            <Modal.Actions>
                <Button >Update Booking</Button>
                <Button> Cancel Booking </Button>
                <Button onClick={() => setbooking(false)}>cancel</Button>
            </Modal.Actions>>

        </Modal>
        <Modal open={unavailable}
               onClose={() => setavailable(false)}
               onOpen={() => setavailable(true)}>
            <Modal.Header>What do you want to change of booking?</Modal.Header>
            <Modal.Actions>
                <Button>Update Unavailibility</Button>
                <Button> Cancel Your Unavailibility </Button>
                <Button onClick={() => setavailable(false)}>cancel</Button>
            </Modal.Actions>>

        </Modal>
        <Button fluid onClick={()=>setbooking(true)}> Update Your Bookings </Button>
            <Button fluid onClick={()=>setavailable(true)} > Update Your Unavailibility</Button>
    </Container>


</>

}
export default Schedule;
