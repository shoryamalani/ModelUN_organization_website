import React, { useState, useEffect,Text } from 'react';
import { BrowserRouter, Link, Switch, Route, useParams } from 'react-router-dom';
import { StyledEngineProvider } from '@mui/material/styles';
// import logo from './logo.svg';
import './App.css';
// import BillView from './BillView';
import NavigationBar from './NavigationBar';
// import Box from '@mui/material/Box';
// import Grid from '@mui/material/Grid'; // Grid version 1
// import Grid from '@mui/material/Unstable_Grid2';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import { GoogleLogin } from 'react-google-login';
import { GoogleOAuthProvider } from '@react-oauth/google';
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const responseGoogle = (response) => {
  console.log(response);
}

function Login() {
  // const [currentTime, setCurrentTime] = useState(0);
  const [login, setLogin] = useState(false);
  
  // const [loading_val, setLoading] = useState(false);
  // useEffect(() => {
  //   fetch('/api/time').then(res => res.json()).then(data => {
  //     setCurrentTime(data.time);
  //   });
  // }, []);
  // useEffect(() => {
  //   fetch('/api/all_bills').then(res => res.json()).then(data => {
  //     console.log(data)
  //     setBills({"results":data});
  //   });
  // },{})

  

  return (
    <GoogleOAuthProvider clientId="533212748008-0n4tlu03uftr9dtshj0i14gokv2f6ijb.apps.googleusercontent.com">
        <GoogleLogin
  onSuccess={credentialResponse => {
    console.log(credentialResponse);
  }}
  onError={() => {
    console.log('Login Failed');
  }}
/>
    </GoogleOAuthProvider>
            
              
            
  );
}


export default Login;

