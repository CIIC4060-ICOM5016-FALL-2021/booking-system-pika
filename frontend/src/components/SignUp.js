// Post new person

import React from "react";
import { Button, Checkbox, Form, Grid, Segment, Header } from "semantic-ui-react";

function SignUp(props) {
  return (
    <>
    <Segment padded='very'>

<Header as='h1'> Sign-Up</Header>
      <Form>
        <Form.Field>
          <label >First Name</label>
          <input placeholder='First Name' />
        </Form.Field>
        <Form.Field>
          <label>Last Name</label>
          <input placeholder='Last Name' />
        </Form.Field>
        <Form.Field>
          <label>Role</label>
          <input placeholder= 'Role '/>
        </Form.Field>
        <Form.Field>
          <label>Email</label>
          <input placeholder= 'Email '/>
          </Form.Field>
        <Form.Field>
          <label>Phone_number</label>
          <input placeholder= 'Phone_number '/>
        </Form.Field>
        <Form.Field>
          <label>Gender</label>
          <input placeholder= 'Gender '/>
        </Form.Field>
        <Form.Field>
          <label>Password</label>
          <input placeholder= 'Password '/>
        </Form.Field>
        <Form.Field>
          <label> Confirm Password</label>
          <input placeholder= 'Confirm'/>
        </Form.Field>
        <Button type='submit'>Submit</Button>
      </Form>

    </Segment>
    </>
  );
}

export default SignUp;