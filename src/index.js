import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import { GoogleOAuthProvider } from '@react-oauth/google';

ReactDOM.render(
<GoogleOAuthProvider clientId="533212748008-0n4tlu03uftr9dtshj0i14gokv2f6ijb.apps.googleusercontent.com">
<React.StrictMode><App /></React.StrictMode></GoogleOAuthProvider>, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
