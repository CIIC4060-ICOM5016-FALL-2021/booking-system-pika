import React, {Component, useEffect, useState} from 'react';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios, {Axios} from "axios";
import {Button,
    Divider,
    Grid,
    Segment,
    Input
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
if (t==false) {
    axios.get('https://booking-system-pika.herokuapp.com/pika-booking/persons/top-bookers').then(res => {

        setBookedPerson(res.data);

        console.log(res.data)
    })
    axios.get('https://booking-system-pika.herokuapp.com/pika-booking/rooms/most-booked').then(res => {
        let BookedRoom = res.data
        setBookedRooms(BookedRoom);

    })
    axios.get('https://booking-system-pika.herokuapp.com/pika-booking/booking/busiesthour').then(res => {
        setBusiestHours(res.data)

    })
    sett(true)
}
    }


        return <>
            <Navbar/>
            {componentDidMount()}
            <Segment>
                <Segment placeholder>
                    <Grid columns={3}stackable textAlign='center'>
                        <Divider></Divider>
                        <Link to = "/BookMeeting" >
                        <button> Create new Booking</button>
                        </Link>
                        <div>
                            <Input action='Search' placeholder='Search...' />
                        </div>
                        <Grid.Row verticalAlign='middle'>
                            <Grid.Column>
                                <h5> Most Booked Person:    {Array.from(Array(BookedPersons.length)).map((_, i) => (
                                    <li>

                                        Bookings:{BookedPersons[i].bookings},
                                       {BookedPersons[i].first_name }  _
                                         {BookedPersons[i].last_name }</li>))}  </h5>
                            </Grid.Column>
                            <h5> Busiest Hours: <ul>{Array.from(Array(BusiestHours.length)).map((_, i) =>(
                                <li>
                                    activebooking: {BusiestHours[i].activebooking},
                                    start_time: {BusiestHours[i].start_time},
                                    end_time: {BusiestHours[i].finish_time}
                                </li>))} </ul>  </h5>
                            <Grid.Column>
                                <h5>Most Booked Room: <ul>{Array.from(Array(BookedRooms.length)).map((_, i) =>(
                                    <li>
                                        r_id:{BookedRooms[i].r_id},
                                        number of bookings: {BookedRooms[i].timed_booked}
                                    </li>))} </ul> </h5>
                                <Link to = "/UserView" > <button>
                                    Go to Userview
                                </button>
                                    </Link>
                                <Link to = "/person" > <button>
                                    Go to Person list
                                </button>
                                </Link>
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </Segment>
            </Segment>
        </>

}



