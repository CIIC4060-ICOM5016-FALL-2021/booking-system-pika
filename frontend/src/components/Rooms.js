import axios from "axios";
import React from "react";


// const baseURL = "https://jsonplaceholder.typicode.com/posts/1";
//
// export default function Rooms() {
//   const [post, setPost] = React.useState(null);
//
//   React.useEffect(() => {
//     axios.get(baseURL).then((response) => {
//       setPost(response.data);
//     });
//   }, []);
//
//   if (!post) return null;
//
//   return (
//     <div>
//       <h1>{post.title}</h1>
//       <p>{post.body}</p>
//     </div>
//   );
// }



// export default class PersonList extends React.Component {
//   state = {
//     persons: []
//   }
//
//   componentDidMount() {
//     axios.get(
//       `https://booking-system-pika.herokuapp.com/pika-booking/rooms`,
//
//     )
//       .then(res => {
//         const persons = res.data;
//         this.setState({ persons });
//       })
//   }
//
//   render() {
//     return (
//       <ul>
//         {
//           this.state.persons
//             .map(person =>
//               <li key={person.id}>{person.r_dept}</li>
//             )
//         }
//       </ul>
//     )
//   }
// }
//



export default class PersonList extends React.Component {
  state = {
    persons: []
  }

  componentDidMount() {



    const requestOptions = {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: 'React POST Request Example' })
    };
    fetch('https://booking-system-pika.herokuapp.com/pika-booking/rooms', requestOptions)
      .then(response => response.json())
      .then(data => this.setState({ postId: data.id }));

    console.log(requestOptions)




  }

  render() {
    return (
      <ul>
        {
          this.state.persons
            .map(person =>
              <li key={person.id}>{person.r_dept}</li>
            )
        }
      </ul>
    )
  }
}



//componentDidMount


function GetAllRooms() {
  this.state = {
    rooms: []
  }




}

function MainRoom() {

}