import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Bar, BarChart, CartesianGrid, Legend, Tooltip, XAxis, YAxis} from "recharts";
import axios, {Axios} from "axios";
import {Button,
    Divider,
    Grid,
    Header,
    Icon,
    Search,
    Segment,
    Dimmer,
    Loader,
    Label,
    Input
} from 'semantic-ui-react'
import {Link, Route} from "react-router-dom";
import bookMeeting from "./BookMeeting";
import Navbar from "./components/Navbar/Navbar";
import UserView from "./UserView";
export default
class Dashboard extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            BookedPersons: [],
            BookedRooms: [],
            BusiestHours: []
        }
    }

    componentDidMount() {

        axios.get('https://booking-system-pika.herokuapp.com/pika-booking/persons/most-booked').then(res=>{
            let BookedPerson = res.data;
            this.setState({BookedPersons:BookedPerson});
            console.log(BookedPerson );
        })
        axios.get('https://booking-system-pika.herokuapp.com/pika-booking/rooms/most-booked').then(res=>{
            let  BookedRoom = res.data
            this.setState({ BookedRooms :BookedRoom});
            console.log(BookedRoom);
        })
        axios.get( 'https://booking-system-pika.herokuapp.com/pika-booking/booking/busiesthour').then(res=>{
            let  Busiest = res.data
            this.setState({ BusiestHours :Busiest });
            console.log(Busiest);
        })
    }
    render(){

        return <>
            <Navbar />
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
                                <h5> Most Booked Person:    {this.state.BookedPersons.map(BookedPerson=>
                                    <li>
                                        Bookings:{BookedPerson.count},
                                       {BookedPerson.p_fname }  _
                                         {BookedPerson.p_lname }</li>)}  </h5>
                            </Grid.Column>
                            <h5> Busiest Hours: <ul>{this.state.BusiestHours.map(Busiest=>
                                <li>
                                    activebooking: {Busiest.activebooking},
                                    start_time: {Busiest.start_time},
                                    end_time: {Busiest.finish_time}
                                </li>)} </ul>  </h5>
                            <Grid.Column>
                                <h5>Most Booked Room: <ul>{this.state.BookedRooms.map(BookedRoom=>
                                    <li>
                                        r_id:{BookedRoom.r_id},
                                        number of bookings: {BookedRoom.timed_booked}
                                    </li>)} </ul> </h5>
                                <Link to = "/UserView" > <button>
                                    Go to Userview
                                </button>
                                    </Link>
                                <Link to = "/person" > <button>
                                    Go to Person list
                                </button>
                                </Link>
                                <Link to = "/rooms" > <button>
                                    Go to room list
                                </button>
                                </Link>
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </Segment>
            </Segment>
        </>
    }
}



