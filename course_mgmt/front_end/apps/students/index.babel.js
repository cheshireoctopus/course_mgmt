var React = require('react')
var createStore = require('redux/store.babel.js')
var actions = require('students/actions.babel')
var Reducer = require('students/reducer.babel')
var Controller = require('redux/controller.jsx')
var Students = require('students/components/controller.jsx')

module.exports = () => {
	let store = createStore(Reducer)

	store.dispatch(actions.setup())

	return React.createElement(Controller, {
		actions,
		store,
		component: Students,
	})
}
