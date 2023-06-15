import React, { useState} from "react";
import axios from "axios";
import {Button,  Form, Grid, Header as SemanticHeader, Modal, Segment} from "semantic-ui-react";
import Navbar from "../Navbar/Navbar";
import {Link} from "react-router-dom";

function SignUp () {

  const [open, setOpen] = useState(false);
    const [r, setr] = useState(false);
  const [fname, setfname] = useState("");
  const [lname, setlname] = useState("");
  const [role, setrole] = useState("");
  const [phone, setphone] = useState("");
  const [gender, setgender] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
const [pen, setopen]= useState(false)

function handlesubmit(){
setopen(true)
}
  const handleChange = () => {
    setOpen(true);
  }
const y = ()=>{
    setr(true)
}
    function first() {
        return !(fname === "" || lname === "" || role === "" || phone === "" || gender === "" || email === "" || password === "");
    }
  function check() {
    if (fname===""||lname===""||role===""||phone===""||gender===""||email===""||password===""||!y){
      return false
    }else {
        let dat = {
            "p_fname": fname,
            "p_lname": lname,
            "p_role": role1(role),
            "p_email": email,
            "p_phone": phone,
            "p_gender": gender2(gender),
            "p_password": password

        }
        console.log(dat)
      axios.post('https://booking-system-pika.herokuapp.com/pika-booking/persons', dat)
        handlesubmit()
      return true
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

    function role1(parameter){
        switch(parameter) {
            case "Student":
                return 1
            case "Professor":
                return 2
            case "Staff":
                return 3

        }
    }

  // componentDidMount() {
  //
  //
  //     var config = {
  //       method: 'post',
  //       url: 'https://booking-system-pika.herokuapp.com/pika-booking/persons',
  //       headers: {
  //         'Content-Type': 'application/json'
  //       },
  //       data : JSON.stringify({
  //         p_fname: "Mr Deez",
  //         p_lname: "Nuitz",
  //         p_email: "deez_two@nuts.com",
  //         p_gender: 1,
  //         p_password: "wownhewice",
  //         p_phone: "747-544-432",
  //         p_role: 2
  //       })
  //     };
  //
  //
  //   axios(config)
  //     .then(function (response) {
  //       console.log("WHY");
  //       console.log(response);
  //       console.log(JSON.stringify(response.data));
  //     })
  //     .catch(function (error) {
  //       console.log(error);
  //     });
  //
  //
  //
  //   (async () => {
  //     await axios(config)
  //       .then(function (response) {
  //         console.log("WHY");
  //         console.log(response);
  //         console.log(JSON.stringify(response.data));
  //       })
  //       .catch(function (error) {
  //         console.log(error);
  //       });
  //
  //   })();
  //
  //
  // }


 return  (
      <>
        <Navbar />
        <Modal
            centered={false}
            open={open}
            onClose={() => setOpen(false)}
            onOpen={() => setOpen(true)}
        >
          <Modal.Header>Invalid!</Modal.Header>
          <Modal.Content>
            <Modal.Description>
              You don't have not submitted all the asked information, please complete all parameters asked.
            </Modal.Description>
          </Modal.Content>
          <Modal.Actions>
            <Button onClick={() => setOpen(false)}>OK</Button>
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
                  <Button onClick={() => check()}>Yes</Button>
              </Modal.Actions>
          </Modal>
        <Grid centered>
          <Grid.Column style={{ maxWidth: 550, marginTop: 20 }}>
            <SemanticHeader>Signup Here</SemanticHeader>


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
                    placeholder="Insert Phone"
                    label="Phone Number"

                  />
                </Form.Field>
                <Form.Field>
                    <Form.Input label='Role'>
                        <select defaultValue={"0"} style={{textAlign: "center"}} onChange={(e) => {setrole(e.target.value);}}>
                            <option key={0} value={"0"}>Select Type</option>
                            {

                                ['Student','Professor', 'Staff'].map((item) => {return <option>{item}</option>})
                            }
                        </select>

                    </Form.Input>
                </Form.Field>
                <Form.Field>
                    <Form.Input label='Gender'>
                        <select defaultValue={"0"} style={{textAlign: "center"}} onChange={(e) => {setgender(e.target.value);}}>
                            <option key={0} value={"0"}>Select Type</option>
                            {

                                ['male','female'].map((item) => {return <option>{item}</option>})
                            }
                        </select>

                    </Form.Input>
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
                <Form.Button content= 'submit' primary onClick={ first()? y :handleChange}/>
                </Segment>
              </Form>



          </Grid.Column>
        </Grid>
          <Modal
          open = {pen} onClose={() => setopen(false)}
          onOpen={() => setopen(true)}>
              <Modal.Header> You have made an account, Please Login</Modal.Header>
              <Link to = "/">
              <Button>Ok</Button>
              </Link>
          </Modal>
      </>
 )

}

export default SignUp
