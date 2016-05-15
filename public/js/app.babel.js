var React = require('react')
var ReactDOM = require('react-dom')
var App = require('./components/app.jsx')
var Classes = require('./apps/classes/index.babel.js')
var assert = require('assert')

module.exports = function (options) {
	assert(options.element)
	assert(options.app)

	let app

	switch (options.app) {
		case ('index'):
			app = React.createElement(App)
			break
		case ('classes'):
			app = new Classes()
			break
		default:
			app = React.createElement(App)
	}

	ReactDOM.render(app, options.element)
}

