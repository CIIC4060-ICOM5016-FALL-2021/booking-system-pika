// Post new person

import React, { useState } from "react";
import { Button, Checkbox, Form, Grid, Segment, Header, Header as SemanticHeader } from "semantic-ui-react";
import Navbar from "../Navbar/Navbar";



// <Segment padded="very" basic>
//
//   <Form>
//     <Form.Field>
//       <label>First Name</label>
//       <input placeholder="First Name" />
//     </Form.Field>
//     <Form.Field>
//       <label>Last Name</label>
//       <input placeholder="Last Name" />
//     </Form.Field>
//     <Form.Field>
//       <label>Role</label>
//       <input placeholder="Role " />
//     </Form.Field>
//     <Form.Field>
//       <label>Email</label>
//       <input placeholder="Email " />
//     </Form.Field>
//     <Form.Field>
//       <label>Phone_number</label>
//       <input placeholder="Phone_number " />
//     </Form.Field>
//     <Form.Field>
//       <label>Gender</label>
//       <input placeholder="Gender " />
//     </Form.Field>
//     <Form.Field>
//       <label>Password</label>
//       <input placeholder="Password " />
//     </Form.Field>
//     <Form.Field>
//       <label> Confirm Password</label>
//       <input placeholder="Confirm" />
//     </Form.Field>
//     <Button type="submit">Submit</Button>
//   </Form>
//
// </Segment>


function SignUp(props) {

  // States for registration
  const [fname, setFName] = useState("");
  const [lname, setLName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("");
  const [password, setPassword] = useState("");


  const options = [
    { key: "m", text: "Male", value: "male" },
    { key: "f", text: "Female", value: "female" },
    { key: "o", text: "Other", value: "other" }
  ];


  return (
    <>
      <Navbar />
      <Grid centered>
        <Grid.Column style={{ maxWidth: 550, marginTop: 20 }}>
          <SemanticHeader>Signup Here</SemanticHeader>

          <Segment>
            <Form>
              <Form.Field>
                <Form.Input
                  fluid
                  name="firstName"
                  placeholder="Insert First Name"
                  label="First Name"

                />
              </Form.Field>
              <Form.Field>
                <Form.Input
                  fluid
                  name="lastName"
                  placeholder="Insert Last Name"
                  label="Last Name"

                />
              </Form.Field>
              <Form.Field>
                <Form.Input
                  fluid
                  icon='email'
                  name="email"
                  placeholder="hello_there@ok.com"
                  label="Email"

                />
              </Form.Field>
              <Form.Field>
                <Form.Input
                  fluid
                  name="telephone"
                  icon='phone'
                  placeholder="Insert Last Name"
                  label="Phone Number"

                />
              </Form.Field>
              <Form.Field>
                <Form.Input
                  fluid
                  name="role"
                  placeholder="Your role in School"
                  label="Role"
                />
              </Form.Field>
              <Form.Field>
                <Form.Select
                  fluid
                  label="Gender wow"
                  options={options}
                  placeholder="Gender"
                />
              </Form.Field>
            </Form>
          </Segment>
          <Button type='submit'>Submit</Button>
        </Grid.Column>

      </Grid>
    </>
  );
}


export default SignUp;