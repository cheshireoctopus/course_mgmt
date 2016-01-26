require('jquery')
require('bootstrap/dist/css/bootstrap.css')

var React = require('react')
var ReactDOM = require('react-dom')

var App = require('./components/app.jsx')
// var App = require('./components/landing/landing.jsx')

var app = React.createElement(App)

ReactDOM.render(app, document.getElementById('app'))
