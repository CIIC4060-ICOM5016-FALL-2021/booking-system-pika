import React, { Component } from 'react'
import Logo from '../../assets/calendar.png';
import {
  Button, Divider, Grid, GridRow, Header, Icon,
  Image,
  Menu, Search,
  Segment

} from "semantic-ui-react";

export default class Navbar extends Component {
  state = { activeItem: 'home' }


  render() {


    return (

      <Segment inverted>
      <Grid columns='equal'>
        <Grid.Column stretched>
          <Segment compact inverted>
            <Image src={Logo} size='mini' rounded />
          </Segment>

        </Grid.Column>
        <Grid.Column >
          <Segment compact inverted floated='right'>
            <Menu inverted pointing secondary>

            </Menu>
          </Segment>
        </Grid.Column>
      </Grid>
      </Segment>

    )
  }
}
