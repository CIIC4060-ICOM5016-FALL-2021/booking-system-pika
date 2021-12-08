import React, {Component, useState} from 'react';
import { Button, Card, Grid, Image,Header } from 'semantic-ui-react';
import axios, {Axios} from "axios";
import {Link} from "react-router-dom";
class UserStatistics extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            UsedRooms: [],
            SharedUser: []
                 }
    }

    componentDidMount() {

        axios.post('https://booking-system-pika.herokuapp.com/pika-booking/persons/person/most-booked-room', {"p_id": '5'}).then(res => {
            let MostUsed = res.data;
            this.setState({UsedRooms: MostUsed});
            console.log(MostUsed);
        })
        axios.post('https://booking-system-pika.herokuapp.com/pika-booking/persons/shared',{"p_id": '5'}).then(res => {
            let SharedUsed = res.data;
            this.setState({SharedUser: SharedUsed});
            console.log(SharedUsed)
        })
        {this.state.UsedRooms.map(MostUsed=>(MostUsed.r_id) )}
        {this.state.SharedUser.map(SharedUsed=>(SharedUsed.p_id))}
    }

    render(){
        return <>
                <h1>  Most Used Room By You:
                 </h1>  )
            <h1>User most booked with You:</h1>
            <div>

            </div>
            <Link to = "/Dashboard" > <button>
                Go to Dashboard
            </button>
            </Link>
            <Link to = "/rooms" > <button>
                Go to room list
            </button>
            </Link>
            <Link to = "/person" > <button>
                Go to Person list
            </button>
            </Link>
        </>
    }
}

export default UserStatistics;