import React from "react";
import {  Card } from 'semantic-ui-react';
import axios from "axios";
export default
class Person extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            person: [] ,
            List : [],
            textflag : false
        };
    }

    componentDidMount() {
        let e = localStorage.getItem("login-data");
      let   data = JSON.parse(e)
        console.log(data.p_id);

axios.post('https://booking-system-pika.herokuapp.com//pika-booking/persons/but-not',{"p_id": data.p_id}).then(res=>{
    let Per=res.data
    this.setState({person: Per});
})
    }
    ToggleButton() {
        this.setState(
            {textflag : !this.state.textflag}
        );
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
     {this.state.person.map(Per=>
                <Card centered={false}>
            <label>{Per.p_fname} _ {Per.p_lname},
                <p>Role: {this.role(Per.p_role)}</p>
                <p> Email: {Per.p_email}</p>
               Gender: { this.gender(Per.p_gender)}
             </label>

                </Card>
          )}

            </>

    }



}