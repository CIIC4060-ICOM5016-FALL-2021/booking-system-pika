import React, {useEffect, useState} from 'react';
import {Calendar, momentLocalizer } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Container, Form, Modal, ModalDescription} from "semantic-ui-react";
import axios from "axios";
import {Book} from "@material-ui/icons";


// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }

function BookMeeting(){
    const [r, setr] = useState(false);
    const [t, sett] = useState(false);
    const [b, setb] = useState(false);
    const [dates, setDates] = useState([]);
    const [open, setOpen] = useState(false);
    const [booking, setbooking] = useState(false);
    const [book, setbook] = useState(false);
    const [unavailable, setavailable] = useState(false);
    const [unavail, setavail] = useState(false);
    const [mark,setmark] = useState(false);
    const localizer = momentLocalizer(moment)
    const [st_dt, setst_dt] = useState("");
    let [et_dt, setet_dt] = useState("");
    const[room_id,setroom_id] = useState("");
    const[invitee,setinvitee]=  useState([]);
    const [g,setg]= useState(false);
    const [its,setits] = useState(false)
    const [Selected,SetSelect] = useState(false)
    const [schedule,setschedule] = useState( [])
    const [info, setinfo] = useState(false);
    const [Edit,setEdit]= useState("")
    const [free, setfree] = useState(false);
    const [updatebooking,setupdatebooking] = useState(false);
    const[deletebooking,setdeletebooking] =useState(false)
    const [updateunavailable,setupunavailable]= useState(false);
    const [deleteunavailable,setdeleteupunavailable]= useState(false);
    const [userfree,setuserfree]= useState(false);
    const [listfree,setlistfree]=useState([]);
    let e = localStorage.getItem("login-data");
    let   dat = JSON.parse(e)
    const[un,setun] =  useState("");
    const [ba_id,setba_id] = useState("");
    const y = ()=>{
        setr(true)
    }


    function getpersonschedule(){
        if (info==false) {
            axios.post('https://booking-system-pika.herokuapp.com/pika-booking/persons/person/all-schedule', {
                person_id: dat.p_id
            }).then(res => {
                setschedule(res.data)
            })
            setinfo(true)
        }
    }

   function getfreeuser(){

   }

    const returnallfalse=()=>{
        setr(false)
        setOpen(false)
        setst_dt("")
        setet_dt("")
        setroom_id("")
        setinvitee([])
        setg(false)
        setbooking(false)
        setbook(false)
        setavailable(false)
        setavail(false)
        setmark(false)
        SetSelect(false)
        setfree(false)
        setinfo(false)
        setb(false)
        setba_id("")
        setun("")
        setdeleteupunavailable(false)
        setupdatebooking(false)
        setr(false)
        setdeletebooking(false)
        setdeleteupunavailable(false)
        sett(false)
        setuserfree(false)

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
    function getfreeinviteetime(){

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
function run(){
        if (Selected== true && open== true||Selected== true && mark== true||Selected== true &&free==true||Selected==true&&unavailable==true
        || Selected==true && booking==true){
            setst_dt(dates[0].startTimeDisplay)
            setet_dt(dates[0].endTimeDisplay)
            return true
        }

        return false
}
    function first() {
        if (st_dt == "" || et_dt == "" || room_id == "" || invitee == []) {
            return false
        } else {
            return true
        }
    }
    function check() {
        if (st_dt == "" || et_dt == "" || room_id == "" || invitee == []||!y){
            return false
        }else {
            let e = localStorage.getItem("login-data");
            let   dat = JSON.parse(e)
            console.log(invitee)
            axios.post('https://booking-system-pika.herokuapp.com//pika-booking/bookings', {
                    "booking_name":ba_id    ,"st_dt": st_dt, "et_dt": et_dt, "host_id": dat.p_id , "invited_id": invitee, "room_id": room_id,

            },
            (error) => {
                console.log(error);
                setEdit("You can't make booking")
                console.log(Edit);
            })
            return true
        }
    }
    function first1() {
        if (st_dt == "" || et_dt == "" ) {
            return false
        } else {
            return true
        }
    }
    function unavailablecheck(){
        if (st_dt == "" || et_dt == "" ||!y){
            return false
        }else {
            let e = localStorage.getItem("login-data");
            let   dat = JSON.parse(e)
            axios.post(' https://booking-system-pika.herokuapp.com/pika-booking/persons/available', {
                "person_id": dat.p_id  ,"st_dt": st_dt, "et_dt": et_dt
            })
            return true
        }
    }
  useEffect(()=>
  {
      getpersonschedule()
      run()
  })
    function Time(year,month, date, hours, minutes){
        if (minutes==0)
       return `${year}-${month +1}-${date} ${hours}:00:00-04`;
        else if (minutes< 10)
            return `${year}-${month +1}-${date} ${hours}:0${minutes}:00-04`;
        else
            return `${year}-${month +1}-${date} ${hours}:${minutes}:00-04`;
    }

    return <Container style={{ height: 800 }}><Calendar
        selectable
        localizer={localizer}
        startAccessor="start"
        events={dates}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
        onSelecting = {(selected) =>{ setDates([{
                        'title': 'Your preferred booking time or unavailable time',
                        'allDay': false,
                        'start': new Date(selected.start),
                        'end': new Date(selected.end),
                        'startTimeDisplay': Time(selected.start.getFullYear(), selected.start.getMonth(),selected.start.getDate(), selected.start.getHours(),selected.start.getMinutes()),
                         'endTimeDisplay': Time(selected.start.getFullYear(), selected.start.getMonth(),selected.start.getDate(),selected.end.getHours(),selected.end.getMinutes())
                    }])
            { console.log(selected.end)};SetSelect(true)} }

    >
    </Calendar>
        <Modal
            centered={false}
            open={t}
            onClose={() => sett(false)}
            onOpen={() => sett(true)}
        >
            <Modal.Header>Invalid!</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    You don't have not submitted all the asked information, please complete all parameters asked.
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => sett(false)}>OK</Button>
            </Modal.Actions>
        </Modal>
        <Modal
            centered={false}
            open={open}
            onClose={() => setOpen(false)}
            onOpen={() => setOpen(true)}
        >
            <Modal.Header>When do you want to book?</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    <Form>
                        <Form.Field>
                            <Form.Input
                        name="Ba_id"
                        placeholder=" Insert Booking id"
                        label="ba_id"
                        value={ba_id}
                        onChange={e => setba_id(e.target.value)}
                            />
                        </Form.Field>
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
                                name="Room Name"
                                placeholder=" Insert Room Name"
                                label="Room Name"
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
                        <Button content='Enter' icon='signup' size='big' onClick={() => (first()?setr(true): sett(true))}/>
                    </Form>
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
            </Modal.Actions>
        </Modal>
        <Modal
            centered={false}
            open={r}
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
                <Button onClick={() => check()&& setg(true)}>Yes</Button>
            </Modal.Actions>
        </Modal>
        <Modal
            centered={false}
            open={its}
            onClose={() => setits(false)}
            onOpen={() => setits(true)}
        >
            <Modal.Header>Room is already booked in selected timeframe. Please select another timeframe.</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setits(false)}>OK</Button>
            </Modal.Actions>
        </Modal>
        <Modal centered={false}
               open={g}
               onClose={() => setg(false)}
               onOpen={() => setg(true)}>
            <Modal.Header>You Have Booked a Room.</Modal.Header>
            <Modal.Actions>
                <Button onClick={() => returnallfalse()}>okay</Button>
            </Modal.Actions>
        </Modal>
        <Modal
            centered={false}
            open={free}
            onClose={() => setfree(false)}
            onOpen={() => setfree(true)}
        >
            <Modal.Header> Please select  timeframe.</Modal.Header>
            <Modal.Content>
                <Modal.Description>
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
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setfree(false)}>OK</Button>
            </Modal.Actions>
        </Modal>
        <Modal
            centered={false}
            open={mark}
            onClose={() => setmark(false)}
            onOpen={() => setmark(true)}
        >
            <Modal.Header>When do you want to be unavailable?</Modal.Header>
            <Modal.Content>
                <Modal.Description>
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
                        <Button content='Enter' icon='signup' size='big' onClick={() => (first1()?setavail(true): sett(true))}/>
                    </Form>
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
            </Modal.Actions>
        </Modal>
        <Modal
            centered={false}
            open={unavail}
            onClose={() => setavail(false)}
            onOpen={() => setavail(true)}
        >
            <Modal.Header>Are you sure?</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setavail(false)}>No</Button>
                <Button onClick={() => unavailablecheck()&& setbook(true)}>Yes</Button>
            </Modal.Actions>
        </Modal>
        <Modal centered={false}
               open={booking}
               onClose={() => setbook(false)}
               onOpen={() => setbook(true)}>
            <Modal.Header>You are unavailable at this hour, {st_dt} to {et_dt}.</Modal.Header>
            <Modal.Actions>
                <Button onClick={() => returnallfalse()}>okay</Button>
            </Modal.Actions>
        </Modal>
        <Container fluid>
        <Button
            fluid
            onClick={() => {setOpen(true)}}
        > Book Meeting </Button>
        <Button
            fluid
            onClick={() => {setmark(true)}}
        > Mark as unavailable</Button>
            <Button fluid onClick={()=>setfree(true)}>Show all free user in time frame</Button>
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
                                name="Booking Name"
                                placeholder=" Insert Booking Name"
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
                    <Button onClick={() => updateunavailablecheck()&& setb(true)}>Yes</Button>
                </Modal.Actions>
            </Modal>
            <Modal open={t}
                   onClose={() => setb(false)}
                   onOpen={() => setb(true)}>
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
            <Modal open = {userfree}
                   onClose={() => setuserfree(false)}
                   onOpen={() => setuserfree(true)}>
                <Button onClick={() => returnallfalse()}>ok</Button>
            </Modal>
    </Container>
    </Container>


}
export default BookMeeting;
