var createStore = require('redux').createStore
var applyMiddleware = require('redux').applyMiddleware
var middleware = require('./middleware.babel.js')

module.exports = reducer => {
	return createStore(reducer, applyMiddleware(...middleware))
}
