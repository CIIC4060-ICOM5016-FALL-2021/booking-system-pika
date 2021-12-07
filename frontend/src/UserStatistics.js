import React, {Component, useState} from 'react';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios, {Axios} from "axios";
class UserStatistics extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            MostUsedRooms: [],
            BookedRooms: []
                 }
    }

    componentDidMount() {


        axios.get('https://booking-system-pika.herokuapp.com/pika-booking/persons/person/most-booked-room', {header:{"p_id": '5'}}).then(res => {
            let MostUsed = res.data;
            this.setState({MostUsedRooms: MostUsed});
            console.log(MostUsed);
        })

    }

    render(){
        return <>
            <h1>Most Used Room By You: { this.state.MostUsedRooms.map(MostUsed=>  <li>( {MostUsed.r_id})</li>
                )} </h1>
            <h1>User most booked with You:</h1>
        </>
    }
}

function GetMostBookedPersonWithUser(props){
    return
}
export default UserStatistics;