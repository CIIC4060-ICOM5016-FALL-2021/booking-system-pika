import React from "react";
import axios from "axios";
import {Button, Card} from "semantic-ui-react";
import Navbar from "./Navbar/Navbar";
import {Link} from "react-router-dom";
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

  ToggleButton() {
    this.setState(
        {textflag : !this.state.textflag}
    );
  }


  render() {
    return <>
      <Navbar />
      {this.state.Room.map(Per=>
          <Card>
            <label>
              Room_id: {Per.r_id}
              <p>Building: {Per.r_building}</p>
              <p> Department: {Per.r_dept}</p>
              Type: { Per.r_type}
            </label>
            <button onClick={()=>addlist(Per)}>Book</button>
            <button onClick={()=>deletelist(Per)}>Unbook</button>
          </Card>
      )}
      <h1> You have booked: {list[0]}</h1>
      <Link to = "/Dashboard" > <button>
        Go to Dashboard
      </button>
      </Link>
      <Link to = "/UserView" > <button>
        Go to Userview
      </button>
      </Link>

      <Link to = "/person" > <button>
        Go to Person list
      </button>
      </Link>
    </>

  }
}
const list = []
function addlist(Per){
  if (list.length==1){
    return
  }else {
    list.push(Per)
    console.log(list)
  }
}
function deletelist(per){
  if (list.length==1&& list.includes(per)){
    list.length =0
  }else
  {
    return "You have not booked a room "
  }

}