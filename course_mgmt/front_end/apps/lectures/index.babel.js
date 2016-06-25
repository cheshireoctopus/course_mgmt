var React = require('react')
var createStore = require('redux/store.babel.js')
var actions = require('lectures/actions.babel')
var Reducer = require('lectures/reducer.babel')
var Controller = require('redux/controller.jsx')
var Lectures = require('lectures/components/controller.jsx')

module.exports = () => {
	let store = createStore(Reducer)

	store.dispatch(actions.setup())

	return React.createElement(Controller, {
		actions,
		store,
		component: Lectures,
	})
}
