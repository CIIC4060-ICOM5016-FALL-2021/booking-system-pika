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
            person: [] ,
            List : []
        };
    }
    componentDidMount() {
axios.post('https://booking-system-pika.herokuapp.com//pika-booking/persons/but-not',{"p_id": 5}).then(res=>{
    let Per=res.data
    this.setState({person: Per});
})
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
                    <button onClick={()=>addlist(Per)}>Invite</button>
                    <button onClick={()=>deletelist(Per)}>UnInvite</button>
                </Card>
          )}
            <h1>  These are the people you have invited:
                </h1>
            <div>{list} </div>
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
const list = []
function addlist(Per){
    if (list.includes(Per)){
        return
    }else {
        list.push(Per)
        console.log(list)
    }
}
function deletelist(per){
    if (list.length==1){
       list.length =0
    }else {
        list.filter(el => el !== per).map(fil => {
            list.splice(0, list.length)
            list.push(fil)
            console.log(list)
        })
    }
}