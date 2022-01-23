import {Button, Form, Modal} from "semantic-ui-react";
import React, {useEffect, useState} from "react";
import {Card, CardHeader, CardContent, IconButton, Typography} from "@material-ui/core";
import {Grid} from 'semantic-ui-react';
import axios from "axios";
import DateTimePicker from 'react-datetime-picker';
import DatePicker from 'react-date-picker';
import {EditOutlined, MoreHorizOutlined} from "@material-ui/icons";



function Rooms(props) {

    const [open, setOpen] = useState();
    const [Building, setBuilding] = useState("");
    const [type, settype] = useState("");
    const [dept, setdept] = useState("");
    const [createdMessage, setCreatedMessage] = useState("");
    const [editMessage, setEditMessage] = useState("");
    const [deleteMessage, setDeleteMessage] = useState("");
    const [roomData, setRoomData] = useState({});
    const [unavailabilityModalOpen, setUnavailabilityModalOpen] = useState(false);
    const [scheduleModalOpen, setScheduleModalOpen] = useState(false);
    const [unavailableTimeSlot, setUnavailableTimeSlot] = useState(new Date());
    const [unavailableTimeSlots, setUnavailableTimeSlots] = useState([]);
    const[]= useState(false);
    const [toMarkAvailable, setToMarkAvailable] = useState("")
    const [invalidTimeSlot, setInvalidTimeSlot] = useState(false)
    const [roomSchedule, setRoomSchedule] = useState(new Date());
    const [allDayRS, setallDayRS] = useState([]);
    const [ CanShowSched,setCanShowSched] = useState(false);
    const [name,setname] = useState("");
    const[i,seti] = useState("");
    const roomID = props.Room_id;
    console.log(roomID)
    const [st, setst_dt] = useState("");
    let [et, setet_dt] = useState("");
   const [roompermission,setroompermision] =useState("");
    const [permission,setpermission] =useState("");
    const[y,sety]= useState("")
    console.log("All day",allDayRS)
    function createRoom(){
        if(  type==="" || Building==="" || dept===""){
            console.log("Empty Field")
            setCreatedMessage("Failed to create room, invalid parameters");
        } else {
            console.log("Creating Room")
            let data = { "r_building": Building,
                "r_name": name,
                "r_dept": dept,
                "r_type": type1(type)}
            axios.post(`https://booking-system-pika.herokuapp.com/pika-booking/rooms`, data
            ).then(
                (response) => {
                    console.log(response);
                    setCreatedMessage("Room Successfully Created");
                    console.log(createdMessage);
                    window.location.reload(false);
                }, (error) => {
                    console.log(error);
                    setCreatedMessage("Failed to create room, invalid parameters");
                }
            );
        }
    }

    function getRoomData(){
        axios.get(`https://booking-system-pika.herokuapp.com/pika-booking/rooms/${roomID}`).then((response) => {
                setRoomData(response.data);
            }, (error) => {
                console.log(error);
            }
        );
    }
function type1(parameter){
        switch(parameter) {
            case 'laboratory':
                return 1
            case 'classroom':
                return 2
            case 'office':
                  return 3
            case'study_space':
                return 4
            case
                'conference_hall':
                return 5
        }

}

    useEffect(() => {
        if(typeof roomID !== "undefined") {
            getRoomData();
        }
    }, []);

    function editRoom() {

            let data = {"r_id": roomID,
                "r_name": y,
                "r_building": i,
                "r_dept": permission,
                "r_type": type1(roompermission)}
            if (y===""){
                data.r_name= roomData.r_name
            }
            if (i === "") {
                data.r_building = roomData.r_building;
            }
            if (permission === "") {
                data.r_dept= roomData.r_dept;
            }
            if (roompermission=== "") {
                data.r_type= type1(roomData.r_type);
            }
            console.log(data)
            axios.put(`https://booking-system-pika.herokuapp.com/pika-booking/rooms`,
                data
            ).then((response) => {
                console.log(response);
                setEditMessage("Changes were made successfully")
                console.log(editMessage);
                window.location.reload(false);
            }, (error) => {
                console.log(error);
                setEditMessage("Changes were not made")
                console.log(editMessage);
            });

    }

    function deleteRoom(){
        axios.delete(`https://booking-system-pika.herokuapp.com/pika-booking/rooms/${roomID}`).then(
            (response) => {
                console.log(response)
                setDeleteMessage("Room deleted successfully");
                console.log(deleteMessage);
                window.location.reload(false);
            }, (error) =>{
                console.log(error);
                setDeleteMessage("Room could not be deleted");
                console.log(deleteMessage)
            }
        );
    }

    function Time(year,month, date, hours, minutes){
        if (minutes===0)
            return `${year}-${month +1}-${date} ${hours}:00:00`;
        else if (minutes< 10)
            return `${year}-${month +1}-${date} ${hours}:0${minutes}:00`;
        else
            return `${year}-${month +1}-${date} ${hours}:${minutes}:00`;
    }
    function markRoom(){
        console.log(st.getMonth())
        console.log(st.getDate())
        let s =Time(st.getFullYear(),st.getMonth(),st.getDate(),st.getHours(),st.getMinutes())
        console.log(s)
       let e = Time(et.getFullYear(),et.getMonth(),et.getDate(),et.getHours(),et.getMinutes())
        const json = {"room_id": roomID,  "st_dt": s,
            "et_dt": e, person_id: JSON.parse(localStorage.getItem('login-data')).p_id};
console.log(json)
        axios.post(`https://booking-system-pika.herokuapp.com/pika-booking/rooms/available`,
            json
        ).then((response) => {
            console.log(response);
            window.location.reload(false);
        },(error) => {
            console.log(error);
        });
    }

    function markRoomAvailable(){
        console.log(toMarkAvailable)


        axios.delete(`https://booking-system-pika.herokuapp.com//pika-booking/rooms/unavailable/ra-id/${toMarkAvailable}`
        ).then((response) => {
            console.log(response);
            window.location.reload(false);
        },(error) => {
            console.log(error);
        });

    }

    function handleChange(date){
        setst_dt(date)
        // console.log(unavailableTimeSlot)
    }
    function handleChange1(date){
        setet_dt(date)
        // console.log(unavailableTimeSlot)
    }
    function handleScheduleChange(date){
        setRoomSchedule(date)
        setallDayRS([]);
    }

    function fetchUnavailableTimeSlots(){
        const url = `https://booking-system-pika.herokuapp.com/pika-booking/rooms/unavailable/${roomID}`;
        axios.get(url, {
            headers: {'Content-Type': 'application/json' }})
            .then(
                (response) => {

                    let unavailableTS = []
console.log(response.data)
                    for(let day of response.data){
                        const st = day.st_dt
                        const et =  day.et_dt
                        console.log(response.data)

                            const w = {start: st, end: et, ra_id: day.ra_id}
                            console.log(w)
                            unavailableTS.push(w)

                    }
                    setUnavailableTimeSlots(unavailableTS);
                    // console.log(unavailableTimeSlots)
                }
            );
    }

    function fetchRoomSchedule(){
        const url = `https://booking-system-pika.herokuapp.com/pika-booking/rooms/available/all-day-schedule`;
        let day = `${roomSchedule.getFullYear()}-${roomSchedule.getMonth() + 1}-${roomSchedule.getDate()}`;
        const data = {"room_id": roomID, "date": day};

        axios.post(url, data,
            {headers: {'Content-Type': 'application/json'}}//text/plain //application/json
        ).then((response) => {
            console.log("Response", response.data);
            let result = []
            let i=0;
            for(let ts of response.data.st_dt){ // data : [ {timeBlock1}, {timeBlock2}, {...} ]
                const blockStart = ` ${response.data.st_dt[i]}-0400 (Atlantic Standard Time)`
                const blockEnd = `${response.data.et_dt[i]}-0400 (Atlantic Standard Time)`;
                const startDate = new Date(blockStart);
                console.log(startDate);
                const endDate = new Date(blockEnd);
                console.log(endDate);
                result.push({start: startDate, end: endDate})
                i++
            }
       console.log(result)
            setallDayRS(result)
        },(error) => {
            console.log(error);
        });
    }

    function formatTime(hours, minutes){
        console.log(hours + " " + minutes)
        let pastNoonIndicator = "";
        if(hours < 12){
            if(hours === 0) hours = 12;
            pastNoonIndicator = "AM";
        }
        else {
            if(hours > 12) hours -= 12;
            pastNoonIndicator = "PM";
        }
        if(minutes === 0){
            return `${hours}:00 ${pastNoonIndicator}`;
        } else {
            return`${hours}:${minutes} ${pastNoonIndicator}`;
        }
    }

    return (

        <div>
            <Card elevation={3}>
                {
                    props.type === "edit" &&
                    <CardHeader
                        action={
                            <IconButton onClick={() => setOpen(true)}><MoreHorizOutlined/></IconButton>
                        }
                        title={props.roomName}
                        subheader={props.building}
                    />
                }

                {
                    props.type === "create" &&
                    <CardHeader
                        action={
                            <IconButton onClick={() => setOpen(true)}><EditOutlined/></IconButton>
                        }
                        title={props.roomName}
                        subheader={props.Building}
                    />
                }
                <CardContent>
                    <Typography variant="body2" color="textSecondary">Room Name: {props.RoomName}</Typography>
                    <Typography variant="body2" color="textSecondary">Building: {props.Building}</Typography>
                    <Typography variant="body2" color="textSecondary">Department: {props.Department}</Typography>
                    <Typography variant="body2" color="textSecondary">Type: {props.Type}</Typography>

                </CardContent>
            </Card>
            <Modal centered={false} open={open} onClose={() => setOpen(false)} onOpen={() => setOpen(true)}>
                {props.type === "create" &&<Modal.Header>Create New Room</Modal.Header>}
                {/*{*/}
                {/*    props.type === "edit" && !unavailabilityModalOpen &&*/}
                {/*    <Modal.Header>*/}
                {/*        Edit Room <br/>*/}
                {/*        <Button onClick={() => {fetchUnavailableTimeSlots(); setUnavailabilityModalOpen(true); }} style={{marginTop: "15px"}}>*/}
                {/*            Change Availability*/}
                {/*        </Button>*/}
                {/*    </Modal.Header>*/}
                {/*}*/}

                {
                    props.type === "edit" && !unavailabilityModalOpen && !scheduleModalOpen &&
                    <Modal.Header>
                        Edit Room <br/>
                        <Button onClick={() => {fetchUnavailableTimeSlots(); setUnavailabilityModalOpen(true); }} style={{marginTop: "15px"}}>
                            Change Availability
                        </Button>
                        <Button onClick={() => {setScheduleModalOpen(true);}} style={{marginTop: "15px"}}>
                            Schedule
                        </Button>
                    </Modal.Header>
                }

                {props.type === "edit" && unavailabilityModalOpen && <Modal.Header>Change availability for {props.roomName}</Modal.Header>}
                {props.type === "edit" && scheduleModalOpen && <Modal.Header>See Schedule for {props.roomName}</Modal.Header>}

                <Modal.Content>
                    {
                        props.type === "create" &&
                        <Modal.Description>
                            <Grid.Column>
                                <Form>
                                    <Form.Input
                                        label="Room Name"
                                        value={name}
                                        onChange={e => setname(e.target.value)}
                                    />
                                    <Form.Input
                                        onChange={(e) => {setBuilding(e.target.value);}}
                                        label='building'
                                    />
                                    <Form.Input label='Type'>
                                        <select defaultValue={"0"} style={{textAlign: "center"}} onChange={(e) => {settype(e.target.value);}}>
                                            <option key={0} value={"0"}>Select Type</option>
                                            {

                                                ['laboratory','classroom', 'office','study_space','conference_hall'].map((item) => {return <option>{item}</option>})
                                            }
                                        </select>

                                    </Form.Input>
                                    <Form.Input label='Deptarment'>
                                        <select defaultValue={"0"} style={{textAlign: "center"}} onChange={(e) => {setdept(e.target.value);}}>
                                            <option key={0} value={"0"}>Select Type</option>
                                            {
                                                [ "ece","mate", "adem","fisi"].map((item) => {return <option>{item}</option>})
                                            }
                                        </select>

                                    </Form.Input>


                                </Form>
                            </Grid.Column>
                        </Modal.Description>
                    }

                    {
                        props.type === "edit" && !unavailabilityModalOpen && !scheduleModalOpen &&
                        <Modal.Description>
                            <Grid.Column>
                                <Form>

                                    <Form.Input
                                        fluid
                                        name="Room Name"
                                        placeholder="Insert Room Name"
                                        label="Room Name"
                                        value={y}
                                        onChange={e => sety(e.target.value)}
                                    />
                                    <Form.Input
                                        fluid
                                        name="Building"
                                        placeholder="Insert Building"
                                        label="building"
                                        value={i}
                                        onChange={e => seti(e.target.value)}
                                    />
                                    <Form.Input label='Department'>
                                        <select defaultValue={"0"} style={{textAlign: "center"}} onChange={(e) => {setpermission(e.target.value);}}>
                                            <option key={0} value={"0"}>Select Type</option>
                                            {

                                                ["ece","mate", "adem","fisi"].map((item) => {return <option>{item}</option>})
                                            }
                                        </select>
                                    </Form.Input>
                                    <Form.Input label='Type'>
                                        <select defaultValue={"0"} style={{textAlign: "center"}} onChange={(e) => {setroompermision(e.target.value);}}>
                                            <option key={0} value={"0"}>Select Type</option>
                                            {

                                                    ['laboratory','classroom', 'office','study_space','conference_hall'].map((item) => {return <option>{item}</option>})
                                            }
                                        </select>

                                    </Form.Input>
                                </Form>
                            </Grid.Column>
                        </Modal.Description>
                    }

                    {
                        props.type === "edit" && unavailabilityModalOpen && !scheduleModalOpen &&
                        <Modal.Description>
                            Select Time Slot to mark unavailable: Start: &nbsp;
                            <DateTimePicker
                                onChange={(e) => handleChange(e)}
                                value={st}
                            />
                            End time:  &nbsp;
                            <DateTimePicker
                                onChange={(e) => handleChange1(e)}
                                value={et}
                            />
                            <br/>
                            Are you sure you want to mark this room as unavailable in the chosen time slot? You will not be able to book any meetings with this room at this time if marked
                            <br/>{<Button onClick={markRoom}>Mark As Unavailable</Button>}
                            <br/><br/>
                            Or select Time Slot to mark available, keep in mind that these time slots are of <strong>30 minutes</strong> in duration <br/>
                            {unavailableTimeSlots.length > 0 &&
                                <select defaultValue={"0"} style={{textAlign: "center"}} onChange={(e) => {
                                    if (e.target.value !== 0) {
                                        setToMarkAvailable(e.target.value);

                                        setInvalidTimeSlot(false);

                                    } else setInvalidTimeSlot(true)
                                }}>
                                    <option key={0} value={"0"}>Select Time Slot</option>
                                    {Array.from(Array(unavailableTimeSlots.length)).map((_, i) => (
                                        <option key={unavailableTimeSlots[i].ra_id} value={unavailableTimeSlots[i].ra_id}>{`${unavailableTimeSlots[i].start} - ${unavailableTimeSlots[i].end}`}</option>
                                    ))}
                                </select>
                            }
                            {unavailableTimeSlots.length === 0 && <p style={{fontSize:"1em"}}>This Room has no time slots marked as unavailable</p>}
                            {invalidTimeSlot && <div style={{color: "red"}}> Please select a time slot</div>}
                            <br/>
                            { unavailableTimeSlots.length > 0 &&
                                <p style={{fontSize: "1em"}}>Are you sure you want to mark this room as available in the chosen time slot? Anyone will be able to book any meetings with this room at this time if marked</p>
                            }

                        </Modal.Description>
                    }

                    {
                        props.type === "edit" && scheduleModalOpen && !unavailabilityModalOpen &&
                        <Modal.Description>
                            Select Day for Room Schedule: &nbsp;
                            <DatePicker
                                onChange={(e) => handleScheduleChange(e)}
                                value={roomSchedule}
                            />
                            <br/><br/>
                            {
                                allDayRS.length > 0 &&
                                <table style={{marginLeft: "auto", marginRight: "auto"}}>
                                    <thead>
                                    <tr>
                                        <th style={{padding:"5px", border: "1px solid black"}} scope={"col"}>Start Time</th>
                                        <th style={{padding:"5px", border: "1px solid black"}} scope={"col"}>End Time</th>
                                        <th style={{padding:"5px", border: "1px solid black"}} scope={"col"}>Available?</th>
                                        <th style={{padding:"5px", border: "1px solid black"}} scope={"col"}>Who Booked?</th>
                                    </tr>
                                    </thead>

                                    <tbody>
                                    {
                                        allDayRS.map(item => {
                                                return (
                                                    <tr>
                                                        <td style={{padding:"5px", border: "1px solid black"}}>{formatTime(item.start.getHours(), item.start.getMinutes())}</td>
                                                        <td style={{padding:"5px", border: "1px solid black"}}>{formatTime(item.end.getHours(), item.end.getMinutes())}</td>
                                                        <td style={{padding:"5px", border: "1px solid black"}}>{"No"}</td>
                                                        <td style={{padding:"5px", border: "1px solid black"}}>{item.user}</td>
                                                    </tr>
                                                )
                                            }
                                        )
                                    }
                                    </tbody>
                                </table>
                            }

                        </Modal.Description>
                    }

                    {props.type === "edit" && !unavailabilityModalOpen && !scheduleModalOpen && <Button onClick={deleteRoom} style={{marginTop: "15px"}}>Delete</Button>}
                    {props.type === "edit" && unavailabilityModalOpen  && unavailableTimeSlots.length > 0 && <Button onClick={markRoomAvailable}>Mark As Available</Button>}




                </Modal.Content>

                <Modal.Actions>
                    {props.type === "create" && <Button onClick={createRoom}>Save</Button>}
                    {props.type === "edit" && !unavailabilityModalOpen && !scheduleModalOpen&&  <Button onClick={editRoom}>Save</Button>}
                    {props.type === "edit" && !unavailabilityModalOpen &&  scheduleModalOpen && <Button onClick={() => setScheduleModalOpen(false)} style={{marginTop: "15px"}}>Cancel</Button>}
                    {props.type === "edit" && !unavailabilityModalOpen && scheduleModalOpen && <Button onClick={() => {fetchRoomSchedule(); setCanShowSched(true);}}>Show Schedule</Button>}
                    {props.type === "edit" && unavailabilityModalOpen && <Button onClick={() => setUnavailabilityModalOpen(false)} style={{marginTop: "15px"}}>Cancel</Button>}

                </Modal.Actions>
            </Modal>
        </div>
    );
}

export default Rooms;