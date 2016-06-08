var createStore = require('redux').createStore
var applyMiddleware = require('redux').applyMiddleware
var middleware = require('redux/middleware.babel.js')

module.exports = reducer => {
	return createStore(reducer, applyMiddleware(...middleware))
}
