import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Form, Modal} from "semantic-ui-react";


// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function BookMeeting(){
    const [dates, setDates] = useState([]);
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment)

    return <Container style={{ height: 800 }}><Calendar
        selectable
        localizer={localizer}
        startAccessor="start"
        events={dates}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
        onSelecting = {(selected) =>{ setDates([{
                        'title': 'Selection',
                        'allDay': false,
                        'start': new Date(selected.start),
                        'end': new Date(selected.end)
                    }] ) } }
    >

    </Calendar>
        <Modal
            centered={false}
            open={open}
            onClose={() => setOpen(false)}
            onOpen={() => setOpen(true)}
        >
            <Modal.Header>When do you want to book?</Modal.Header>
            <Modal.Content>
                <Modal.Description>
                    <Form>
                        <Form.Field>
                            <Form.Input
                                fluid
                                name="Start time"
                                placeholder="Insert Start time"
                                label="Start time"

                            />
                        </Form.Field>
                        <Form.Field>
                            <Form.Input
                                fluid
                                name="End time"
                                placeholder="Insert End time"
                                label="End time"

                            />
                        </Form.Field>
                        <Form.Field>
                            <Form.Input
                                fluid
                                icon='r_id'
                                name="r_id"
                                placeholder=" Insert r_id"
                                label="Room ID"

                            />
                        </Form.Field>
                        <Form.Field>
                            <Form.Input
                                fluid
                                icon='Invitee_id'
                                name="Invitee_id"
                                placeholder=" Insert Invitee_id"
                                label="Invitee_id"

                            />
                        </Form.Field>
                    </Form>
                </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpen(false)}>OK</Button>
            </Modal.Actions>
        </Modal>
        <Container fluid>
        <Button
            fluid
            onClick={() => {setOpen(true)}}
        > Book Meeting </Button>
        <Button
            fluid
            onClick={() => {setOpen(true)}}
        > Mark as unavailable</Button>
    </Container>
    </Container>


}
export default BookMeeting;
