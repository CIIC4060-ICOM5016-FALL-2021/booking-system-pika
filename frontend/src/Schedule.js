import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Modal, ModalContent, ModalDescription, Segment} from "semantic-ui-react";
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
    const [ba_id,setba_id] = useState("");
    const [st_dt, setst_dt] = useState("");
    const [et_dt, setet_dt] = useState("");
    const[room_id,setroom_id] = useState("");
    const[invitee,setinvitee]=  useState("");
    const[un,setun] =  useState("");
    const [updatebooking,setupdatebooking] = useState(false);
    const[deletebooking,setdeletebooking] =useState(false)
    const [updateunavailable,setupunavailable]= useState(false);
    const [deleteunavailable,setdeleteupunavailable]= useState(false);
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
    function updatebookingcheck(){
        let e = localStorage.getItem("login-data");
        let   dat = JSON.parse(e)
        if (st_dt == "" || et_dt == "" || room_id == "" || invitee == ""||ba_id==""||!r){
            return false
        }else{
            axios.put("https://booking-system-pika.herokuapp.com/pika-booking/booking", {
                "b_id": ba_id,
                "st_dt": st_dt,
                "et_dt": et_dt,
                "host_id": dat,
                "invited_id": invitee,
                "room_id": room_id
            })
            return true
        }
    }
    function updateunavailablecheck(){
        let e = localStorage.getItem("login-data");
        let   dat = JSON.parse(e)
        if (st_dt == "" || et_dt == "" || un==""||!r){
            return false
        }else{
            axios.put(" https://booking-system-pika.herokuapp.com/pika-booking/persons/available", {
                "person_id":  dat,
                "st_dt": st_dt,
                "et_dt": et_dt
            })
            return true
        }
    }
    function deletebookingcheck(){
        if (ba_id==""||!r){
            return false
        }else{
            axios.delete(" https://booking-system-pika.herokuapp.com/pika-booking/booking")
            return true
        }
    }
    function deleteunavailablegcheck(){
        if (un==""||!r){
            return false
        }else{
            axios.delete(" https://booking-system-pika.herokuapp.com/pika-booking/persons/available")
            return true
        }
    }
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
                <Button onClick={()=>setupdatebooking(true)}>Update Booking</Button>
                <Button onClick={()=>setdeletebooking(true)}> Cancel Booking </Button>
                <Button onClick={() => setbooking(false)}>cancel</Button>
            </Modal.Actions>>

        </Modal>
        <Modal open={updatebooking}
               onClose={() => setupdatebooking(false)}
               onOpen={() => setupdatebooking(true)}>
            <Modal.Header>What do you want to change of booking?</Modal.Header>
            <Modal.Content>
            <Modal.Description>
                <Form.Field>
                <Form.Input
                    fluid
                    name="Ba_id"
                    placeholder=" Insert Booking id"
                    label="ba_id"
                    value={ba_id}
                    onChange={e => setba_id(e.target.value)}

                />
            </Form.Field>
                <Form>
                    <Form.Field>
                        <Form.Input
                            fluid
                            name="Start time"
                            placeholder="Insert Start time"
                            label="Start time"
                            value={st_dt}
                            onChange={e => setst_dt(e.target.value)}
                        />
                    </Form.Field>
                    <Form.Field>
                        <Form.Input
                            fluid
                            name="End time"
                            placeholder="Insert End time"
                            label="End time"
                            value={et_dt}
                            onChange={e => setet_dt(e.target.value)}
                        />
                    </Form.Field>
                    <Form.Field>
                        <Form.Input
                            fluid
                            name="r_id"
                            placeholder=" Insert r_id"
                            label="Room ID"
                            value={room_id}
                            onChange={e => setroom_id(e.target.value)}
                        />
                    </Form.Field>
                    <Form.Field>
                        <Form.Input
                            fluid
                            name="Invitee_id"
                            placeholder=" Insert Invitee_id"
                            label="Invitee_id"
                            value={invitee}
                            onChange={e => setinvitee(e.target.value)}

                        />
                    </Form.Field>
                    <Button content='Enter' icon='signup' size='big'/>
                </Form>
            </Modal.Description>
                </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setupdatebooking(false)}>cancel</Button>
            </Modal.Actions>
        </Modal>
        <Modal open={deletebooking}
               onClose={() => setdeletebooking(false)}
               onOpen={() => setdeletebooking(true)}>
            <Modal.Header>which booking do you want to delete?</Modal.Header>
            <Modal.Content>
                <ModalDescription>
                    <Form.Field>
                        <Form.Input
                            fluid
                            name="Ba_id"
                            placeholder=" Insert Booking id"
                            label="ba_id"
                            value={ba_id}
                            onChange={e => setba_id(e.target.value)}

                        />
                    </Form.Field>

                </ModalDescription>

            </Modal.Content>
            <Modal.Actions>
                <Button content='Confirm'/>
                <Button onClick={() => setdeletebooking(false)}>cancel</Button>
            </Modal.Actions>>

        </Modal>
        <Modal open={unavailable}
               onClose={() => setavailable(false)}
               onOpen={() => setavailable(true)}>
            <Modal.Header>What do you want to change of your free time?</Modal.Header>
            <Modal.Actions>
                <Button onClick={()=>setupunavailable(true)}>Update Unavailibility</Button>
                <Button onClick={() => setdeleteupunavailable(true)}> Cancel Your Unavailibility </Button>
                <Button onClick={() => setavailable(false)}>cancel</Button>
            </Modal.Actions>>

        </Modal>
    <Modal open={updateunavailable}
           onClose={() => setupunavailable(false)}
           onOpen={() => setupunavailable(true)}>
        <Modal.Header>What do you want to change of your free time?</Modal.Header>
        <Modal.Content>
                <Modal.Description>
                    <Form.Field>
                        <Form.Input
                            fluid
                            name="unavailable id"
                            placeholder=" Insert Unavailable Id"
                            label="unavailable id"
                            value={un}
                            onChange={e => setun(e.target.value)}

                        />
                    </Form.Field>
                    <Form>
                        <Form.Field>
                            <Form.Input
                                fluid
                                name="Start time"
                                placeholder="Insert Start time"
                                label="Start time"
                                value={st_dt}
                                onChange={e => setst_dt(e.target.value)}
                            />
                        </Form.Field>
                        <Form.Field>
                            <Form.Input
                                fluid
                                name="End time"
                                placeholder="Insert End time"
                                label="End time"
                                value={et_dt}
                                onChange={e => setet_dt(e.target.value)}
                            />
                        </Form.Field>
                    </Form>
            </Modal.Description>
        </Modal.Content>
        <Modal.Actions>
            <Button onClick={() => setupunavailable(false)}>cancel</Button>
            <Button content='Confirm'/>
        </Modal.Actions>
    </Modal>
        <Modal open={deleteunavailable}
               onClose={() => setdeleteupunavailable(false)}
               onOpen={() => setdeleteupunavailable(true)}>
            <Modal.Header>Which free time do you want to delete?</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    <Form.Field>
                        <Form.Input
                            fluid
                            name="unavailable id"
                            placeholder=" Insert Unavailable Id"
                            label="unavailable id"
                            value={un}
                            onChange={e => setun(e.target.value)}

                        />
                    </Form.Field>
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setdeleteupunavailable(false)}>cancel</Button>
                <Button content='Confirm'/>
            </Modal.Actions>>
        </Modal>
        <Button fluid onClick={()=>setbooking(true)}> Update Your Bookings </Button>
            <Button fluid onClick={()=>setavailable(true)} > Update Your Unavailibility</Button>
    </Container>


</>

}
export default Schedule;
