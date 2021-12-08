import React from "react";
import axios from "axios";
import {Button, Card} from "semantic-ui-react";
export default
class Room extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      Room: []
    };
  }
  componentDidMount() {
    axios.get('https://booking-system-pika.herokuapp.com/pika-booking/rooms').then(res=>{
      let Per=res.data
      this.setState({Room: Per});
    })
  }



  render() {
    return <>

      {this.state.Room.map(Per=>
          <Card>
            <label>
              Room_id: {Per.r_id}
              <p>Building: {Per.r_building}</p>
              <p> Department: {Per.r_dept}</p>
              Type: { Per.r_type}
            </label>
            <Button basic color='green'>
              Book
            </Button>
          </Card>
      )}

    </>

  }
}
