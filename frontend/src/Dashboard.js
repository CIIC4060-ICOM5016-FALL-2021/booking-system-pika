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
} from 'semantic-ui-react'
import bookMeeting from "./BookMeeting";
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
            console.log(Busiest)
        })
    }
    render(){

        return <>
            <Segment>

                <Segment placeholder>
                    <Grid columns={3}stackable textAlign='center'>
                        <Divider></Divider>

                        <Grid.Row verticalAlign='middle'>
                            <Grid.Column>
                                <h1> Most Booked Person: <ul>   {this.state.BookedPersons.map(BookedPerson=>
                                    <li>
                                        Bookings:{BookedPerson.count},
                                         {BookedPerson.p_fname }  _
                                         {BookedPerson.p_lname },
                                        id: {BookedPerson.p_id}</li>)} </ul> </h1>



                            </Grid.Column>
                            <h1> Busiest Hours: <ul>{this.state.BusiestHours.map(Busiest=>
                                <li>
                                    activebooking: {Busiest.activebooking},
                                    start_time: {Busiest.start_time},
                                    end_time: {Busiest.finish_time}
                                </li>)} </ul>  </h1>
                            <Grid.Column>
                                <h1>Most Booked Room: <ul>{this.state.BookedRooms.map(BookedRoom=>
                                    <li>
                                        r_id:{BookedRoom.r_id},
                                        number of bookings: {BookedRoom.timed_booked}
                                    </li>)} </ul> </h1>

                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </Segment>
            </Segment>
            <button> Back to main menu  </button>
        </>
    }
}



