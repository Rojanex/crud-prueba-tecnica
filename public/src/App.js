import React from 'react';
import axios from 'axios';
import Swal from 'sweetalert2';

class App extends React.Component {
  
  constructor(props){
    super(props)
    this.state={
      users: [],
      type_dni: '',
      dni:'',
      name:'',
      last_name:'',
      hobbie:'',
      _id:0
    }
  }


  componentDidMount(){
    axios.get('http://localhost:5000/users')
    .then((res) => 
      this.setState({
        'users': res.data,
        'type_dni': '',
        'dni':'',
        'name':'',
        'last_name':'',
        'hobbie':'',
        '_id':0
      })
    )
    
  }
  
  
  namechange = event => {
    this.setState({
      name:event.target.value
    })
  }

  last_namechange = event => {
    this.setState({
      last_name:event.target.value
    })
  }


  dnichange = event => {
    this.setState({
      dni:event.target.value
    })
  }


  type_dnichange = event => {
    this.setState({
      type_dni:event.target.value
    })
  }

  hobbiechange = event => {
    this.setState({
      hobbie:event.target.value
    })
  }

  submit(event, id){
    event.preventDefault()
    //console.log(id)
    if(id===0){
      axios.post('http://localhost:5000/users', {
        'type_dni':this.state.type_dni,
        'dni':this.state.dni,
        'name':this.state.name, 
        'last_name':this.state.last_name,  
        'hobbie':this.state.hobbie,      
      })
      .then((res)=> {
        console.log(res.data)
        if(res.data.message === 'Usuario Creado'){
          Swal.fire(
            'Nuevo Usuario',
            res.data.message,
            'success'
          );
        }
        this.componentDidMount();
      })
    }else{
      axios.patch(`http://localhost:5000/users/${id}`, {
        type_dni:this.state.type_dni,
        dni:this.state.dni,
        name:this.state.name, 
        last_name:this.state.last_name,  
        hobbie:this.state.hobbie     
      })
      .then((res)=>{
        if(res.data.message === 'Usuario Actualizado'){
          Swal.fire(
            'Edicion de Usuario',
            res.data.message,
            'success'
          );
        }
        this.componentDidMount();
      })
    }

  }



  delete(id){
    axios.delete(`http://localhost:5000/users/${id}`)
    .then(()=>{
      this.componentDidMount();
    })

  }

  get(id){
    //console.log(id)
    axios.get(`http://localhost:5000/${id}`)
    .then((res)=>{
      console.log(res.data)
      this.setState({
        type_dni:res.data.type_dni,
        dni:res.data.dni,
        name:res.data.name,
        last_name:res.data.last_name,
        hobbie:res.data.hobbie,
        _id:res.data._id
        
      })
    })

  }


  
 render(){
  return (
    <div className='container mt-5'>
      <div className='row mt-5'>
        <div className='col lg-6 mt-5'>
          <form onSubmit={(e) => {this.submit(e, this.state._id)}}>
            <div className='form-group'>
              <input type="text" onChange={(e)=> {this.type_dnichange(e)}} className='form-control' placeholder='Tipo de Documento' value={this.state.type_dni}/>
            </div>
            <div className='form-group'>
              <input type="text" onChange={(e)=> {this.dnichange(e)}} className='form-control' placeholder='Documento' value={this.state.dni}/>
            </div>
            <div className='form-group'>
              <input type="text" onChange={(e)=> {this.namechange(e)}} className='form-control' placeholder='Nombres' value={this.state.name}/>
            </div>
            <div className='form-group'>
              <input type="text" onChange={(e)=> {this.last_namechange(e)}} className='form-control' placeholder='Apellidos' value={this.state.last_name}/>
            </div>
            <div className='form-group'>
              <input type="text" onChange={(e)=> {this.hobbiechange(e)}} className='form-control' placeholder='Hobbie' value={this.state.hobbie}/>
            </div>
            <button className='btn btn-block btn-primary'>Enviar</button>
            
          </form>
        </div>
        <div className='col lg-6 mt-5'>
          <table className='table'>
            <thead>
              <th> Tipo de Documento</th>
              <th> Documento</th>
              <th> Nombres</th>
              <th> Apellidos</th>
              <th> Hobbie</th>
              <th> Editar</th>
              <th> Eliminar</th>
            </thead>
            <tbody>
              
              
            {this.state.users.map(user => 
              <tr>
                <td>{user.type_dni}</td>
                <td>{user.dni}</td>
                <td>{user.name}</td>
                <td>{user.last_name}</td>
                <td>{user.hobbie}</td>
                <td>
                  <button onClick={(e)=> {this.get(user._id)}} className='btn btn-sm btn-primary'>
                  <i className='fa fa-pencil'></i>
                  </button>
                </td>
                <td>
                  <button onClick={(e)=> {this.delete(user._id)}} className='btn btn-sm btn-danger'>
                  <i className='fa fa-trash'></i>
                  </button>
                </td>
              </tr>

              )}
              



            </tbody>
          </table>
        </div>
        
      </div>
    </div>
  );
              }
            }
                 


export default App;
