import React, {Component, useState} from 'react';
import {Calendar, momentLocalizer, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import moment from 'moment';
import {Button, Card, Container, Modal, Segment} from "semantic-ui-react";
import {Link} from "react-router-dom";


// Event {
//     title: string,
//         start: Date,
//         end: Date,
//         allDay?: boolean
//     resource?: any,
// }


function Schedule(){
    const [dates, setDates] = useState([{
        'title': 'Selection',
        'allDay': false,
        'start': new Date(moment.now()),
        'end': new Date(moment.now())
    }]);
    const [open, setOpen] = useState(false);
    const localizer = momentLocalizer(moment)

    return <>
    <Container style={{ height: 800 }}><Calendar
        localizer={localizer}
        startAccessor="start"
        events={dates}
        endAccessor="end"
        views={["month", "day"]}
        defaultDate={Date.now()}
    >

    </Calendar>
    </Container>
        <Segment>
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
    </Segment>
</>

}
export default Schedule;
