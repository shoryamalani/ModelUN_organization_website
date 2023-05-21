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
import { GoogleLogin,GoogleLogout } from 'react-google-login';
import env from 'react-dotenv';
import { gapi, loadAuth2 } from 'gapi-script';
import { UserCard } from './UserCard';
import { Button } from '@material-ui/core';
import './Login.css';
import { Redirect } from 'react-router-dom/cjs/react-router-dom.min';
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
//   const [login, setLogin] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const setAuth2 = async () => {
      const auth2 = await loadAuth2(gapi, process.env.REACT_APP_CLIENT_ID, '')
      if (auth2.isSignedIn.get()) {
          updateUser(auth2.currentUser.get())
      } else {
          attachSignin(document.getElementById('customBtn'), auth2);
      }
    }
    setAuth2();
  }, []);

  useEffect(() => {
    if (!user) {
      const setAuth2 = async () => {
        const auth2 = await loadAuth2(gapi, process.env.REACT_APP_CLIENT_ID, '')
        attachSignin(document.getElementById('customBtn'), auth2);
      }
      setAuth2();
    }
  }, [user])

  const updateUser = (currentUser) => {
    const name = currentUser.getBasicProfile().getName();
    const profileImg = currentUser.getBasicProfile().getImageUrl();
    setUser({
      name: name,
      profileImg: profileImg,
    });
    fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: name,
                profileImg: profileImg,
                userToken: currentUser.getAuthResponse().id_token,
                email: currentUser.getBasicProfile().getEmail(),
                }),
            })
            .then((res) => res.json())
            .then((data) => {
                console.log(data);
            }
            );
    
  };

  const attachSignin = (element, auth2) => {
    auth2.attachClickHandler(element, {},
      (googleUser) => {
        updateUser(googleUser);
      }, (error) => {
      console.log(JSON.stringify(error))
    });
  };

  const signOut = () => {
    const auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(() => {
      setUser(null);
      console.log('User signed out.');
    });
  }

  if(user) {
    return (
      <div className="container">
        <UserCard user={user} />
        <Button variant='contained' id="" className="btn logout" onClick={signOut}>
          Logout
        </Button>
      </div>
    );
  }

  return (
    <div className="container">
      <Button variant='contained' id="customBtn" className="btn login" >
        Login
      </Button>
    </div>
  );

            
              
            
}


export default Login;

