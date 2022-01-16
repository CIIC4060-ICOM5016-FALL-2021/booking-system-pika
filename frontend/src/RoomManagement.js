import React, {useEffect, useState} from "react";
import Navbar from "./components/Navbar/Navbar";
import {Button} from 'semantic-ui-react';
import {Container, Grid, Card} from 'semantic-ui-react';
import {Link} from "react-router-dom";

import axios from "axios";
import Rooms from "./components/Rooms";



function RoomManagement(){
    const [isAuth, setIsAuth] = useState(true)
    const [rooms, setRooms] = useState([]);
    const data = localStorage.getItem('login-data');
    const user = JSON.parse(data);

    function getAuthentication() {

        if (user.role == 3) {
            setIsAuth(true);
        }
    }

    function fetchRooms(){
        axios.get(`https://booking-system-pika.herokuapp.com/pika-booking/rooms`).then((response) => {
                setRooms(response.data);
            }, (error) => {
                console.log(error);
            }
        );
    }
    useEffect(() => {
        getAuthentication();
        fetchRooms();
    }, []);

    if(isAuth) {
        return (
            <>
                <Navbar/>
                <h1 style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>Rooms</h1>
                <Container>
                    <Grid container spacing={3}>
                        {Array.from(Array(rooms.length)).map((_, i) => (
                            <Rooms

                                Room_id= {`${rooms[i].r_id}`}
                                Building= {`${rooms[i].r_building}`}
                                Department= {`${rooms[i].r_dept}`}
                                Type= {`${rooms[i].r_type}`}
                                type={"edit"}/>
                        ))}
                        <Grid justify={"center"} container item xs={12} md={6} lg={4}>
                            <Rooms
                                roomName={`Create`}
                                building={`New Room`}
                                type={"create"}
                            />
                        </Grid>

                    </Grid>
                </Container>
            </>
        );
    } else {
        return (
            <>
                <Navbar/>
                <h3 style={{color: "red", display: 'flex', justifyContent: 'center', alignItems: 'center'}}>You are not
                    allowed to manage rooms, please contact a Department Staff to make any changes</h3>
                <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                    <Link to={"/"}>
                        <Button content='Go Home' icon='home' size='big' color="violet"/>
                    </Link>
                </div>
            </>
        );
    }
}

export default RoomManagement;