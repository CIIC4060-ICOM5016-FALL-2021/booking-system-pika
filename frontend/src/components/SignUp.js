// Post new person

import React from "react";
import { Button, Checkbox, Form, Grid, Segment } from "semantic-ui-react";

function SignUp(props) {
  return (
    <>
    <Segment padded='very'>
      <Form>
        <Form.Field>
          <label>First Name</label>
          <input placeholder='First Name' />
        </Form.Field>
        <Form.Field>
          <label>Last Name</label>
          <input placeholder='Last Name' />
        </Form.Field>
        <Form.Field>
          <Checkbox label='I agree to the Terms and Conditions' />
        </Form.Field>
        <Button type='submit'>Submit</Button>
      </Form>
    </Segment>
    </>
  );
}

export default SignUp;