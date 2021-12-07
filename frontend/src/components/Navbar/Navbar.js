// import React from "react";
// import { Button, Image, Segment } from "semantic-ui-react";
// import Logo from '../../assets/logo.svg';
// import '../../themes/Navbar.css';
// import MenuExampleInvertedSecondary from "./MenuItems";
//
// const ImageExampleRounded = () => (
//   <Image src={Logo} size='mini' rounded />
// )
//
// function Navbar(props) {
//
//   return (
//     <Segment inverted color='blue'>
//       <Button floated='right'>Sign Up</Button>
//       <ImageExampleRounded/>
//       <MenuExampleInvertedSecondary/>
//     </Segment>
//   );

// <Image src={Logo} size='mini' rounded />

// }



import React, { Component } from 'react'
import Logo from '../../assets/calendar.png';
import {
  Button, Divider, Grid, GridRow, Header, Icon,
  Image,
  Menu, Search,
  Segment

} from "semantic-ui-react";

export default class MenuExampleInvertedSecondary extends Component {
  state = { activeItem: 'home' }

  handleItemClick = (e, { name }) => this.setState({ activeItem: name })

  render() {
    const { activeItem } = this.state

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
              <Menu.Item
                name='home'
                active={activeItem === 'home'}
                onClick={this.handleItemClick}
              />
              <Menu.Item
                name='statistics'
                active={activeItem === 'statistics'}
                onClick={this.handleItemClick}
              />
              <Menu.Item
                name='signup'
                active={activeItem === 'signup'}
                onClick={this.handleItemClick}
              />
            </Menu>
          </Segment>

        </Grid.Column>
      </Grid>
      </Segment>

    )
  }
}




// <Segment inverted>
//   <Image src={Logo} size='mini' rounded />
// </Segment>
// <Segment inverted>
//   <Menu>
//     <Menu.Item
//       name='Home'
//     />
//     <Menu.Item
//       name='Home'
//     />
//     <Menu.Item
//       name='Home'
//     />
//   </Menu>
// </Segment>