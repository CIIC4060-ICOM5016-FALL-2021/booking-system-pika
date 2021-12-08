import React,{Component, useState}  from "react";
import { Button, Card, Grid, Image,Header } from 'semantic-ui-react';
import axios from "axios";
import Navbar from "./Navbar/Navbar";
import {Link} from "react-router-dom";
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
    getemail(){

      let email =this.state.person.map(Per=> (Per.p_email))
        return email
    }
    getpassword(){
       let password= this.state.person.map(Per=> (Per.p_password))
        return password
    }
    getid(){
        let id= this.state.person.map(Per=> (Per.p_id))
        return id
    }
    gender(parameter){
        switch(parameter) {
            case 1:
                return "Male"
            case 2:
                return "Female"

        }
    }

    role(parameter){
        switch(parameter) {
            case 1:
                return "Student"
            case 2:
                return "Professor"
            case 3:
                return "Staff"
            default:
                return "Visitor"
        }
    }
    render() {
        return <>
            <Navbar />
     {this.state.person.map(Per=>
                <Card>
            <label>{Per.p_fname} _ {Per.p_lname},
                <p>Role: {this.role(Per.p_role)}</p>
                <p> Email: {Per.p_email}</p>
               Gender: { this.gender(Per.p_gender)}
             </label>
                    <Button basic color='green'>
                        Invite
                    </Button>
                </Card>
          )}
            <Link to = "/Dashboard" > <button>
                Go to Dashboard
            </button>
            </Link>
            <Link to = "/UserView" > <button>
                Go to Userview
            </button>
            </Link>
            <Link to = "/rooms" > <button>
                Go to room list
            </button>
            </Link>
            </>

    }
}
