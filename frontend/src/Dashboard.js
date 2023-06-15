import React, { useEffect, useState} from 'react';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from "axios";
import {
    Grid,
    Segment,
} from 'semantic-ui-react'
import {Link} from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";
export default
function Dashboard(){



        const [BookedPersons, setBookedPerson] = useState([]);
        const [BookedRooms, setBookedRooms] = useState([]);
    const [ BusiestHours, setBusiestHours] = useState([]);
    const [t,sett]= useState(false);
   function  componentDidMount() {
if (t===false) {
    axios.get('https://booking-system-pika.herokuapp.com/pika-booking/persons/most-booked').then(res => {

        setBookedPerson(res.data);

        console.log(res.data)
    })
    axios.get('https://booking-system-pika.herokuapp.com/pika-booking/rooms/most-booked').then(res => {
        let BookedRoom = res.data
        setBookedRooms(BookedRoom);
console.log(BookedRoom)
    })
    axios.get('https://booking-system-pika.herokuapp.com/pika-booking/booking/busiesthour').then(res => {
        setBusiestHours(res.data)
        console.log(res.data)
    })
    sett(true)
}
    }

useEffect(()=> {
    componentDidMount()
})
        return <>
            <Navbar/>
            <Segment>
                <Segment placeholder>
                    <Grid columns={3} stackable textAlign='center'>
                        <Grid.Row verticalAlign='middle'>
                            <Grid.Column>
                                <h5> Most Booked Person:
                                    <li>
                                        <table style={{marginLeft: "auto", marginRight: "auto"}}>
                                            <thead>
                                            <tr>
                                                <th style={{padding:"5px", border: "1px solid black"}} scope={"col"}>Number of bookings</th>
                                                <th style={{padding:"5px", border: "1px solid black"}} scope={"col"}>Person name</th>


                                            </tr>
                                            </thead>

                                            <tbody>
                                            {
                                                BookedPersons.map(item => {
                                                        return (
                                                            <tr>
                                                                <td style={{padding:"5px", border: "1px solid black"}}>{item.count}</td>
                                                                <td style={{padding:"5px", border: "1px solid black"}}>{item.p_fname}_{item.p_lname}</td>
                                                            </tr>
                                                        )
                                                    }
                                                )
                                            }
                                            </tbody>
                                        </table>
                                            </li>
                                    </h5>

                            </Grid.Column>
                            <h5> Busiest Hours: <ul> <li>
                                <table style={{marginLeft: "auto", marginRight: "auto"}}>
                                    <thead>
                                    <tr>
                                        <th style={{padding:"5px", border: "1px solid black"}} scope={"col"}>Number of bookings</th>
                                        <th style={{padding:"5px", border: "1px solid black"}} scope={"col"}>Start Time</th>
                                        <th style={{padding:"5px", border: "1px solid black"}} scope={"col"}>End Time</th>


                                    </tr>
                                    </thead>

                                    <tbody>
                                    {
                                        BusiestHours.map(item => {
                                                return (
                                                    <tr>
                                                        <td style={{padding:"5px", border: "1px solid black"}}>{item.activebooking}</td>
                                                        <td style={{padding:"5px", border: "1px solid black"}}>{item.start_time}</td>
                                                        <td style={{padding:"5px", border: "1px solid black"}}>{item.finish_time}</td>
                                                    </tr>
                                                )
                                            }
                                        )
                                    }
                                    </tbody>
                                </table>
                            </li>


                     </ul>  </h5>
                            <Grid.Column>
                                <h5>Most Booked Room: <ul><table style={{marginLeft: "auto", marginRight: "auto"}}>
                                    <thead>
                                    <tr>
                                        <th style={{padding:"5px", border: "1px solid black"}} scope={"col"}>Times Booked</th>
                                        <th style={{padding:"5px", border: "1px solid black"}} scope={"col"}>Room Name</th>


                                    </tr>
                                    </thead>

                                    <tbody>
                                    {
                                        BookedRooms.map(item => {
                                                return (
                                                    <tr>
                                                        <td style={{padding:"5px", border: "1px solid black"}}>{item.timed_booked}</td>
                                                        <td style={{padding:"5px", border: "1px solid black"}}>{item.r_name}</td>
                                                    </tr>
                                                )
                                            }
                                        )
                                    }
                                    </tbody>
                                </table> </ul> </h5>
                                <Link to = "/UserView" > <button>
                                    Go to Userview
                                </button>
                                    </Link>
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </Segment>
            </Segment>
        </>

}



