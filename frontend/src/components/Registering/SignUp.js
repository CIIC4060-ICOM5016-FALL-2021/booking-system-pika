import React, { Component } from "react";
import axios from "axios";
import { Button, Card, Form, Grid, Header as SemanticHeader, Segment } from "semantic-ui-react";
import Navbar from "../Navbar/Navbar";


class SignUp extends Component {
  state = {
    fname: '',
    lname: '',
    email: '',
    role: '',
    phone: '',
    gender: '',
    password: '',
    submittedfname: '',
    submittedlname: '',
    submittedemail: '',
    submittedrole: '',
    submittedphone: '',
    submittedgender: '',
    submittedpassword: ''
  }

  options = [
    { key: 0, text: "Male", value: 0 },
    { key: 1, text: "Female", value: 1 },
    { key: 2, text: "Other", value: 2 }
  ];


  handleChange = (e, { name, value }) => this.setState({ [name]: value }, () => {
    const { fname, lname, email, role, phone, gender, password } = this.state

  })

  handleSubmit = () => {
    const { fname, lname, email, role, phone, gender, password } = this.state

    this.setState({
      submittedfname: fname,
      submittedlname: lname,
      submittedrole: role,
      submittedphone: phone,
      submittedgender: gender,
      submittedpassword: password,
      submittedemail: email
    });
    console.log(this.state.submittedfname)


    let config = {
      method: 'post',
      url: 'https://booking-system-pika.herokuapp.com/pika-booking/persons',
      headers: {
        'Content-Type': 'application/json'
      },
      data : JSON.stringify({
        p_fname: this.state.submittedfname,
        p_lname: this.state.submittedlname,
        p_role: this.state.submittedrole,
        p_email: this.state.submittedemail,
        p_password: this.state.submittedpassword,
        p_phone: this.state.submittedphone,
        p_gender: this.state.submittedgender
      })
    };

    (async () => {
      await axios(config)
        .then(function (response) {
          console.log("WHY");
          console.log(response);
          console.log(JSON.stringify(response.data));
        })
        .catch(function (error) {
          console.log(error);
        });

    })();


  }
handleQuery = () => {



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


  render() {
    const {
      fname,
      lname,
      email,
      role,
      phone,
      gender,
      password,
      submittedfname,
      submittedlname,
      submittedemail,
      submittedrole,
      submittedphone,
      submittedgender,
      submittedpassword
    } = this.state

    return (
      <>
        <Navbar />
        <Grid centered>
          <Grid.Column style={{ maxWidth: 550, marginTop: 20 }}>
            <SemanticHeader>Signup Here</SemanticHeader>

            <Segment>
              <Form onSubmit={this.handleSubmit}>
                <Form.Field>
                  <Form.Input
                    fluid
                    name="fname"
                    value={fname}
                    icon='user'
                    placeholder="Insert First Name"
                    label="First Name"
                    onChange={this.handleChange}
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
                    onChange={this.handleChange}
                  />
                </Form.Field>
                <Form.Field>
                  <Form.Input
                    fluid
                    onChange={this.handleChange}
                    value={email}
                    icon='mail'
                    name="email"
                    placeholder="hello_there@ok.com"
                    label="Email"

                  />
                </Form.Field>
                <Form.Field>
                  <Form.Input
                    fluid
                    onChange={this.handleChange}
                    value={phone}
                    name="phone"
                    icon='phone'
                    placeholder="Insert Last Name"
                    label="Phone Number"

                  />
                </Form.Field>
                <Form.Field>
                  <Form.Input
                    fluid
                    onChange={this.handleChange}
                    value={role}
                    name="role"
                    placeholder="Your role in School"
                    label="Role"
                  />
                </Form.Field>
                <Form.Field>
                  <Form.Input
                    fluid
                    onChange={this.handleChange}
                    value={gender}
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
                    onChange={this.handleChange}
                    value={password}
                    name="password"
                    icon='asterisk'
                    placeholder="Type password"
                    label="Password"
                  />
                </Form.Field>
                <Form.Button type='submit'>Submit</Form.Button>
              </Form>
            </Segment>

            <pre>{JSON.stringify({ fname, email, gender }, )}</pre>
            <pre>{JSON.stringify({ submittedfname, submittedemail }, )}</pre>
          </Grid.Column>
        </Grid>
      </>
    )
  }
}

export default SignUp
