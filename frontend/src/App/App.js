import React from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Header from '../Registration/Header/Header';
import RegistrationForm from '../Registration/RegistrationForm/RegistrationForm';
import AuthenticationForm from '../Auth/Authentification';
import Menu from '../Menu/Menu';


const App = () => {
    return (<div className='wrapper'>
        <Router>
            <Routes>
                <Route index element={<div><Header showAccount={false}/><AuthenticationForm/></div>}/>
                <Route path="/RegistrationForm"
                       element={<div><Header showAccount={false}/><RegistrationForm/></div>}/>
                <Route path="/auth"
                       element={<div><Header showAccount={false}/><AuthenticationForm/></div>}/>

                <Route path="/menu"
                       element={<div><Header showContactInfo={true}/><Menu/></div>}/>
            </Routes>
        </Router>
    </div>);
};

export default App;