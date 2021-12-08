import React,{Component, useState}  from "react";
import { Button, Card, Grid, Image,Header } from 'semantic-ui-react';
import axios from "axios";
export default
class Person extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            person: []
        };
    }
    componentDidMount() {
axios.get('https://booking-system-pika.herokuapp.com/pika-booking/persons').then(res=>{
    let Per=res.data
    this.setState({person: Per});
})
    }
    render() {
        return <>

     {this.state.person.map(Per=>
                <Card>
            <label>{Per.p_fname} _ {Per.p_lname},
                <p>Role: {Per.p_role}</p>
                <p> Email: {Per.p_email}</p>
               Gender: {Per.p_gender}
             </label>
                    <Button basic color='green'>
                        Invite
                    </Button>
                </Card>
          )}

            </>

    }
}
