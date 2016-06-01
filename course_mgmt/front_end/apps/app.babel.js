var ReactDOM = require('react-dom')
var React = require('react')
var Main = require('./main.jsx')
var assert = require('assert')

module.exports = options => {
	assert(options.element)
	assert(options.app)

	let props = {
		app: options.app
	}

	let main = React.createElement(Main, props)

	ReactDOM.render(main, options.element)
}

