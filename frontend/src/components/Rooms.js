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
    const [toMarkAvailable, setToMarkAvailable] = useState(new Date())
    const [invalidTimeSlot, setInvalidTimeSlot] = useState(false)
    const [roomSchedule, setRoomSchedule] = useState(new Date());
    const [allDayRS, setallDayRS] = useState([]);
    const [canShowSched, setCanShowSched] = useState(false);
    const [Room_id,setroomid] =useState("");
    const roomID = props.id;
    const [st, setst_dt] = useState("");
    let [et, setet_dt] = useState("");
   const [roompermission,setroompermision] =useState("");
    console.log("All day",allDayRS)
    function createRoom(){
        if(  type==="" || Building==="" || dept===""){
            console.log("Empty Field")
            setCreatedMessage("Failed to create room, invalid parameters");
        } else {
            console.log("Creating Room")
            let data = { "r_building": Building,
                "r_dept": dept,
                "r_type": type}
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
        axios.get(`https://booking-system-pika.herokuapp.com/pika-booking/rooms/id/${roomID}`).then((response) => {
                setRoomData(response.data);
            }, (error) => {
                console.log(error);
            }
        );
    }


    useEffect(() => {
        if(typeof roomID !== "undefined") {
            getRoomData();
        }
    }, []);

    function editRoom() {
        if(Building===""  && dept === "" &&  type==="0"){
            console.log("No changes")
            setEditMessage("No changes where made");
        } else {
            let data = {"r_id": 1,
                "r_building": Building,
                "r_dept": dept,
                "r_type": type}
            // console.log(data);
            if (Building === "") {
                data.r_building = roomData.r_building;
            }
            if (dept === "") {
                data.r_dept= roomData.r_dept;
            }
            if (dept === "") {
                data.r_dept= roomData.r_dept;
            }
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


    function markRoom(){

        const json = {rid: roomID,  "st_dt": st,
            "et_dt": et, person_id: JSON.parse(localStorage.getItem('login-data')).p_id};

        axios.post(`https://booking-system-pika.herokuapp.com/pika-booking/rooms/availablee`,
            json,
            {headers: {'Content-Type': 'application/json'}}
        ).then((response) => {
            console.log(response);
            window.location.reload(false);
        },(error) => {
            console.log(error);
        });
    }

    function markRoomAvailable(){
        console.log(toMarkAvailable)
        const json = { "r_id": roomID,
            "st_dt": st,
            "et_dt": et}

        axios.delete('https://booking-system-pika.herokuapp.com/pika-booking/rooms/available', {
            data: json,
            headers: {'Content-Type': 'application/json'}}//text/plain //application/json
        ).then((response) => {
            console.log(response);
            window.location.reload(false);
        },(error) => {
            console.log(error);
        });

    }

    function handleChange(date){
        setUnavailableTimeSlot(date)
        // console.log(unavailableTimeSlot)
    }

    function handleScheduleChange(date){
        setRoomSchedule(date)
        setallDayRS([]);
    }

    function fetchUnavailableTimeSlots(){
        const url = `https://booking-system-pika.herokuapp.com/pika-booking/rooms/available/schedule${roomID}`;
        axios.get(url, {
            headers: {'Content-Type': 'application/json' }})
            .then(
                (response) => {
                    // console.log(`Time Slot fetched for ${roomID}: `, JSON.stringify(response.data))
                    let unavailableTS = []
                    // console.log("Response: ", response.data)
                    const days = Object.keys(response.data)
                    for(let day of days){ // day: [ {timeBlock1}, {timeBlock2}, {...} ]
                        let tempDate = day.split('-');
                        const blockStart = response.data[day][0].start.split(":");
                        const startDate = new Date(tempDate[0], tempDate[1] - 1, tempDate[2], parseInt(blockStart[0]), parseInt(blockStart[1]), parseInt(blockStart[2]));
                        unavailableTS.push(startDate)
                    }
                    setUnavailableTimeSlots(unavailableTS);
                    // console.log(unavailableTimeSlots)
                }
            );
    }

    function fetchRoomSchedule(){
        const url = `https://booking-system-pika.herokuapp.com/pika-booking/rooms/available/all-day-schedule`;
        let day = `${roomSchedule.getFullYear()}-${roomSchedule.getMonth() + 1}-${roomSchedule.getDate()}`;
        const inject = {"room_id": roomID, "date": day};
        console.log(inject)
        axios.post(url, inject,
            {headers: {'Content-Type': 'application/json'}}//text/plain //application/json
        ).then((response) => {
            console.log("Response", response.data);
            const timeSlots = response.data
            let result = []
            for(let ts of timeSlots){ // data : [ {timeBlock1}, {timeBlock2}, {...} ]
                const blockStart = ts.tstarttime.split(":");
                const blockEnd = ts.tendtime.split(":");
                const startDate = new Date(roomSchedule.getFullYear(), roomSchedule.getMonth() + 1, roomSchedule.getDate(), parseInt(blockStart[0]), parseInt(blockStart[1]), parseInt(blockStart[2]));
                const endDate = new Date(roomSchedule.getFullYear(), roomSchedule.getMonth() + 1, roomSchedule.getDate(), parseInt(blockEnd[0]), parseInt(blockEnd[1]), parseInt(blockEnd[2]));
                result.push({start: startDate, end: endDate, available: ts.available, user: ts.user})
            }
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
                        subheader={props.building}
                    />
                }
                <CardContent>

                    <Typography variant="body2" color="textSecondary">Capacity: {props.capacity}</Typography>
                    <Typography variant="body2" color="textSecondary">Permission: {props.permission}</Typography>
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
                                        onChange={(e) => {setdept(e.target.value);}}
                                        label='Department'
                                    />
                                    <Form.Input
                                        onChange={(e) => {setBuilding(e.target.value)}}
                                        label='Building Name'
                                    />
                                    <Form.Input label='Type'>
                                        <select defaultValue={"0"} style={{textAlign: "center"}} onChange={(e) => {settype(e.target.value);}}>
                                            <option key={0} value={"0"}>Select Permission</option>
                                            {
                                                [ 1,2, 3,4, 5].map((item) => {return <option>{item}</option>})
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

                                    <h5 style={{paddingTop: "5px"}}>Building Name</h5>
                                    <p style={{paddingBottom: "5px"}}>{`${props.Building}`}</p>
                                    <h5 style={{paddingTop: "5px"}}>Department</h5>
                                    <p style={{paddingBottom: "5px"}}>{`${props.Department}`}</p>
                                    <Form.Input label='Permission'>
                                        <select defaultValue={"0"} style={{textAlign: "center"}} onChange={(e) => {setroompermision(e.target.value);}}>
                                            <option key={0} value={"0"}>Select Permission</option>
                                            {
                                                [1,2, 3,4, 5, 6].map((item) => {return <option>{item}</option>})
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
                            Select Time Slot to mark unavailable: &nbsp;
                            <DateTimePicker
                                onChange={(e) => handleChange(e)}
                                value={unavailableTimeSlot}
                            />
                            <br/>
                            Are you sure you want to mark this room as unavailable in the chosen time slot? You will not be able to book any meetings with this room at this time if marked
                            <br/>{<Button onClick={markRoom}>Mark As Unavailable</Button>}
                            <br/><br/>
                            Or select Time Slot to mark available, keep in mind that these time slots are of <strong>30 minutes</strong> in duration <br/>
                            {unavailableTimeSlots.length > 0 &&
                                <select defaultValue={"0"} style={{textAlign: "center"}} onChange={(e) => {
                                    if (e.target.value != 0) {
                                        setToMarkAvailable(new Date(e.target.value));
                                        setInvalidTimeSlot(false);
                                        {
                                            console.log(e.target.value)
                                        }
                                    } else setInvalidTimeSlot(true)
                                }}>
                                    <option key={0} value={"0"}>Select Time Slot</option>
                                    {Array.from(Array(unavailableTimeSlots.length)).map((_, i) => (
                                        <option>{`${unavailableTimeSlots[i].toDateString()}, ${unavailableTimeSlots[i].toLocaleTimeString()}`}</option>
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
                                                        <td style={{padding:"5px", border: "1px solid black"}}>{item.available.toString() === "true" ? "Yes" : "No"}</td>
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