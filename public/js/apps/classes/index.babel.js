var React = require('react')
var createStore = require('redux').createStore
var actions = require('./actions.babel')
var Reducer = require('./reducer.babel')
var Controller = require('../redux/controller.jsx')
var Classes = require('./components/controller.jsx')

module.exports = function (options) {
    let store = createStore(Reducer)

    // store.dispatch(actions.setup(options))

    return React.createElement(Controller, {
        actions,
        store,
        component: Classes,
    })
}
