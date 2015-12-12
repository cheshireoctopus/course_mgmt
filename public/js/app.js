require('jquery')
require('bootstrap/dist/css/bootstrap.css')

var React = require('react')
var ReactDOM = require('react-dom')

var App = require('./components/app.jsx')

var app = React.createElement(App)
var el = document.getElementById('app')

ReactDOM.render(app, el)
