var _ = require('underscore')
var React = require('react')
var Immutable = require('immutable')
var Redux = require('redux')

module.exports = React.createClass({
    displayName: 'Controller',

    propTypes: {
        store: React.PropTypes.shape({
            dispatch: React.PropTypes.func.isRequired,
            getState: React.PropTypes.func.isRequired,
            subscribe: React.PropTypes.func.isRequired,
        }).isRequired,
        actions: React.PropTypes.objectOf(React.PropTypes.func.isRequired).isRequired,
        component: React.PropTypes.func.isRequired,
    },

    componentWillMount () {
        this._unsubscribe = this.props.store.subscribe(() => {
            this.setState({
                storeState: this.props.store.getState(),
            })
        })
    },

    componentWillUnmount () {
        this._unsubscribe()
    },

    getInitialState () {
        return {
            storeState: this.props.store.getState(),
            actions: Redux.bindActionCreators(this.props.actions, this.props.store.dispatch),
        }
    },

    shouldComponentUpdate (nextProps, nextState) {
        return !Immutable.is(this.state.storeState, nextState.storeState) || this.props.component !== nextProps.component
    },

    render () {
        var props = _.extend(
            {},
            this.state.storeState.toJS(),
            this.state.actions
        )

        return React.createElement(this.props.component, props)
    },
})
