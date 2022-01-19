import {Link} from "react-router-dom";
import React, {useEffect, useState} from 'react';
import {
    Button,

    Form,
    Grid, Header as SemanticHeader,

    Modal,
    Segment
} from 'semantic-ui-react';
import axios from "axios";
import Navbar from "./components/Navbar/Navbar";


function Settings() {
    const [open, setOpen] = useState(false);
    const [t, sett] = useState(false);
    const [r, setr] = useState(false);
    const [e, sete] = useState(false);
    const [g,setg] = useState(false);
    const [info, setinfo] = useState(false);
    const [fname, setfname] = useState("");
    const [lname, setlname] = useState("");
    const [phone, setphone] = useState("");
    const [gender, setgender] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    let [data, setdata] = useState("");
    let [name, setname] = useState("");



    const handleChange = () => {
        setOpen(true);
    }
    const y = () => {
        setr(true)
    }
    const q = () => {
        sett(true)
    }

    function getinfo() {
        if (info===false) {
            let e = localStorage.getItem("login-data");
            let dat = JSON.parse(e)
            axios.get( `https://booking-system-pika.herokuapp.com/pika-booking/persons/${dat.p_id}`).then(res => {
                setname(res.data)
            })
            setinfo(true)
            console.log(name)
        }

    }

    function deleteact() {
        if (t === true) {
            let e = localStorage.getItem("login-data");
            let dat = JSON.parse(e)
            axios.delete(`https://booking-system-pika.herokuapp.com/pika-booking/persons/${dat.p_id}`)
            localStorage.removeItem("login-data")
            return "deleted"
        }
    }
    const returnallfalse=()=>{
        setr(false)
        setOpen(false)
        sete(false)
        setfname("")
        setlname("")
        setphone("")
        setgender("")
        setEmail("")
        setPassword("")
        setr(false)

        sett(false)
    }
    function check() {

        if ( !y) {
            return false
        } else {
            let e = localStorage.getItem("login-data");
            let dat = JSON.parse(e)
            data = {"p_id": dat.p_id,
                "p_fname": fname,
                "p_lname": lname,
                "p_role": name.p_role,
                "p_email": email,
                "p_phone": phone,
                "p_gender": gender2(gender),
                "p_password": password}
            if (fname ==="") {
              data.p_fname= name.p_fname
              console.log(fname);
            }
            if (lname===""){
                data.p_lname=name.p_lname;
            }
            if (email===""){
                data.p_email=name.p_email;

            }
            if (phone===""){
                data.p_phone=name.p_phone;
            }
            if (gender===""){
                data.p_gender=name.p_gender;
            }
            if (password===""){
                data.p_password=name.p_password;
            }
            axios.put('https://booking-system-pika.herokuapp.com/pika-booking/persons', data).then(res => {
                setdata(res.data);
            })
            window.location.reload(false);
            console.log(data);
            return true
        }
    }
    function gender1(parameter){
        switch(parameter) {
            case 1:
                return "Male"
            case 2:
                return "Female"

        }
    }
    function gender2(parameter){
        switch(parameter) {
            case "male":
                return 1
            case "female":
                return 2

        }
    }
    function Role(parameter) {
        switch (parameter) {
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
    useEffect(()=>{getinfo()})
        return (
            <>

                <Modal
                    centered={false}
                    open={open}
                    onClose={() => setOpen(false)}
                    onOpen={() => setOpen(true)}
                >
                    <Modal.Header>To Update!</Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                            <Form>
                                <Segment>
                                    <Form.Field>
                                        <Form.Input
                                            fluid
                                            name="fname"
                                            value={fname}
                                            onChange={e => setfname(e.target.value)}
                                            icon='user'
                                            placeholder="Insert First Name"
                                            label="First Name"
                                        />
                                    </Form.Field>
                                    <Form.Field>
                                        <Form.Input
                                            icon='user'
                                            fluid
                                            name="lname"
                                            value={lname}
                                            placeholder="Insert Last Name"
                                            label="Last Name"
                                            onChange={e => setlname(e.target.value)}
                                        />
                                    </Form.Field>
                                    <Form.Field>
                                        <Form.Input
                                            fluid
                                            value={email}
                                            onChange={e => setEmail(e.target.value)}
                                            icon='mail'
                                            name="email"
                                            placeholder="hello_there@ok.com"
                                            label="Email"

                                        />
                                    </Form.Field>
                                    <Form.Field>
                                        <Form.Input
                                            fluid
                                            value={phone}
                                            onChange={e => setphone(e.target.value)}
                                            name="phone"
                                            icon='phone'
                                            placeholder="Insert Last Name"
                                            label="Phone Number"

                                        />
                                    </Form.Field>
                                    <Form.Field>
                                        <Form.Input
                                            fluid
                                            value={gender}
                                            onChange={e => setgender(e.target.value)}
                                            name="gender"
                                            icon='other gender'
                                            placeholder="I Identify As"
                                            label="Gender"
                                        />
                                    </Form.Field>
                                    <Form.Field>
                                        <Form.Input
                                            type="password"
                                            fluid
                                            value={password}
                                            onChange={e => setPassword(e.target.value)}
                                            name="password"
                                            icon='asterisk'
                                            placeholder="Type password"
                                            label="Password"
                                        />
                                    </Form.Field>
                                </Segment>
                            </Form>
                        </Modal.Description>
                    </Modal.Content>
                    <Modal.Actions>
                        <Button onClick={() => setOpen(false)}>NO</Button>
                        <Button onClick={y}>Yes</Button>
                    </Modal.Actions>
                </Modal>
                <Modal
                    centered={false}
                    open={r}
                    onClose={() => setr(false)}
                    onOpen={() => setr(true)}
                >
                    <Modal.Header>Are you sure?</Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                        </Modal.Description>
                    </Modal.Content>
                    <Modal.Actions>
                        <Button onClick={() => setr(false)}>No</Button>
                        <Button onClick={() => check() && sete(true)}>Yes</Button>
                    </Modal.Actions>
                </Modal>
                <Modal     centered={false}
                           open={e}
                           onClose={() => sete(false)}
                           onOpen={() => sete(true)}>
                    <Modal.Header>You have updated you info</Modal.Header>
                    <Button onClick={() => returnallfalse()}>Ok</Button>
                </Modal>
                <Modal
                    centered={false}
                    open={t}
                    onClose={() => sett(false)}
                    onOpen={() => sett(true)}
                >
                    <Modal.Header>Are you sure?</Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                        </Modal.Description>
                    </Modal.Content>
                    <Modal.Actions>
                        <Button onClick={() => sett(false)}>No</Button>
                        <Button onClick={() => deleteact()&& setg(true)}>Yes</Button>
                    </Modal.Actions>
                </Modal>
                <Modal
                    centered={false}
                    open={g}
                    onClose={() => setg(false)}
                    onOpen={() => setg(true)}
                >
                    <Modal.Header>You have deleted your account</Modal.Header>
                    <Modal.Content>
                        <Modal.Description>
                        </Modal.Description>
                    </Modal.Content>
                    <Modal.Actions>
                        <Link to = "/" > <button>
                          Ok
                        </button>
                        </Link>
                    </Modal.Actions>
                </Modal>

                <h1>Account Info</h1>
                <h2 aria-checked={true}> First Name: {name.p_fname}</h2>
                <h2> Last Name: {name.p_lname}</h2>
                <h2> Email: {name.p_email}</h2>
                <h2> Role: {Role(name.p_role)}</h2>
                <h2> Gender: {gender1(name.p_gender)}</h2>
                <h2> Phone: {name.p_phone}</h2>
                <Grid >
                    <Grid.Column style={{maxWidth: 200, marginTop: 20}}>
                        <SemanticHeader>Account Options</SemanticHeader>
                        <Form>
                            <Segment>
                                <Form.Field>

                                    <Form.Button content='Update Account' primary onClick={handleChange}/>
                                </Form.Field>
                                <Form.Field>

                                    <Form.Button content='Delete Account' primary onClick={q}/>
                                </Form.Field>
                            </Segment>
                        </Form>


                    </Grid.Column>
                </Grid>
            </>

        )


}
export default Settings;