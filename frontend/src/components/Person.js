import React,{Component, useState}  from "react";
import { Button, Card, Image,Header } from 'semantic-ui-react';
class Person extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            person: []
        };
    }
    componentDidMount() {

    }
    render() {
        return(
        <Card.Group>
            <Card>
     ]{this.state.person.map(Per=>
          <Header> {Per.fname} _ {Per.lname} </Header>,
                <p> {Per.email}</p>,
                <p> {Per.gender}</p>

          )}
                <Button basic color='green'>
                    Invite
                </Button>
            </Card>
    </Card.Group>
        )
    }
}
export default  Person;