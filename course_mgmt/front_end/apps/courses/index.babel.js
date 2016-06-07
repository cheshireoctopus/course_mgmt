var React = require('react')
var createStore = require('../redux/store.babel.js')
var actions = require('./actions.babel')
var Reducer = require('./reducer.babel')
var Controller = require('../redux/controller.jsx')
var Courses = require('./components/controller.jsx')

module.exports = options => {
    let store = createStore(Reducer)

    store.dispatch(actions.setup(options))

    return React.createElement(Controller, {
        actions,
        store,
        component: Courses,
    })
}
