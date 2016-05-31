var ReactDOM = require('react-dom')
var Classes = require('./classes/index.babel.js')
var Students = require('./students/index.babel.js')
var assert = require('assert')

module.exports = options => {
	assert(options.element)
	assert(options.app)

	let app

	switch (options.app) {
		case ('classes'):
			app = new Classes()
			break
		case ('students'):
			app = new Students()
			break
		default:
			app = new Classes()
	}

	ReactDOM.render(app, options.element)
}

