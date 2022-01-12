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
    const [t,sett] = useState(false)
    const [r, setr] = useState(false);
    const [booking, setbooking] = useState(false);
    const [unavailable, setavailable] = useState(false);
    const [mark,setmark] = useState([]);
    const [ba_id,setba_id] = useState("");
    const [st_dt, setst_dt] = useState("");
    const [et_dt, setet_dt] = useState("");
    const[room_id,setroom_id] = useState("");
    const[invitee,setinvitee]=  useState("");
    const[un,setun] =  useState("");
    const[date,setdate] =  useState("");
    const [updatebooking,setupdatebooking] = useState(false);
    const[deletebooking,setdeletebooking] =useState(false)
    const [updateunavailable,setupunavailable]= useState(false);
    const [deleteunavailable,setdeleteupunavailable]= useState(false);
    const [meetings,setmeetings] =useState([])
    let e = localStorage.getItem("login-data");
    let   dat = JSON.parse(e)
    const [dates, setDates] = useState([{
        'title': 'Selection',
        'allDay': false,
        'start': new Date(moment.now()),
        'end': new Date(moment.now()),
    }]);
    const [info, setinfo] = useState(false);
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment)


    const [schedule1,setschedule1] =  useState([{
        'title': 'Selection',
        'allDay': false,
        'start': new Date(moment.now()),
        'end': new Date(moment.now()),
    }])
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

                const w = {title: "Event", 'allDay': false , 'start':  new Date(st), 'end':  new Date(et)}
                t.push(w)
                    i=i+1
            }
                setmeetings(t)
        })
    }



    }

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



    function Time(year,month, date, hours, minutes){
        if (minutes==0)
            return `${year}-${month +1}-${date} ${hours}:00:00-04`;
        else if (minutes< 10)
            return `${year}-${month +1}-${date} ${hours}:0${minutes}:00-04`;
        else
            return `${year}-${month +1}-${date} ${hours}:${minutes}:00-04`;
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
    function updateunavailablecheck(){

        if (st_dt == "" || et_dt == "" || un==""||!r){
            return false
        }else{
            axios.put(" https://booking-system-pika.herokuapp.com/pika-booking/persons/available", {
                "pa_id" : un,
                "person_id":  dat.p_id,
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
        <Modal
            centered={false}
            open={open}
            onClose={() => setOpen(false)}
            onOpen={() => setOpen(true)}
        >
            <Modal.Header>Invalid!</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    You don't have not submitted all the asked information, please complete all parameters asked.
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpen(false)}>OK</Button>
            </Modal.Actions>
        </Modal>
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
            <Button content='Confirm'
                    onClick={() => {check()? setOpen(true):setr(true)} }/>
        </Modal.Actions>
    </Modal>
        <Modal open={r}
               onClose={() => setr(false)}
               onOpen={() => setr(true)}
        >
        <Modal.Header>Are you sure?</Modal.Header>
        <Modal.Content>
            <Modal.Description>
            </Modal.Description>
        </Modal.Content>
        <Modal.Actions>
            <Button onClick={() => setr(false)}>No</Button>
            <Button onClick={() => updateunavailablecheck()&& sett(true)}>Yes</Button>
        </Modal.Actions>
    </Modal>
    <Modal open={t}
               onClose={() => sett(false)}
               onOpen={() => sett(true)}>
        <Modal.Header>You have updated your unavailable timeslot</Modal.Header>
        <Modal.Actions>
            <Button onClick={() => returnallfalse()}>Ok</Button>
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
