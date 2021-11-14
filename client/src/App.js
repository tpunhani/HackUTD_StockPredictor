import './App.css';
import {useState, useEffect} from 'react'
import NavigationBar from './components/js/NavigationBar';
import { BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import SignIn from './components/js/SignIn'
import SignUp from './components/js/SignUp';

import PublicRoute from './components/utils/PublicRoute';

import { getUser } from './components/utils/Common';
import Footer from './components/js/footer/Footer'

import Chart1 from './components/js/charts/Chart1';

 // GET USER INFORMATION FROM DATABASE SHOWING 1 FOR TRUE AND 0 FOR FALSE

function App(token) {


  const [isAdmin, setIsAdmin] = useState();


  useEffect(() => {
    if(getUser() != null){
      setIsAdmin(getUser().isAdmin)
    }
    

  }, [isAdmin])


  return (
    <Router>
      <Switch>
        <Route path='/' exact >
          <NavigationBar/>
          <Chart1/>
          <Footer />
        </Route>
        <PublicRoute path='/sign-in' component={SignIn}/>
        <Route path='/sign-up' component={SignUp}/>
      </Switch>
    </Router>
  );
}

export default App;
