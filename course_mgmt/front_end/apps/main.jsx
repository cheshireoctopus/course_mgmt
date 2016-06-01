var React = require('react')
var ReactDOM = require('react-dom')
var Nav = require('./nav/components/controller.jsx')
var Classes = require('./classes/index.babel')
var Students = require('./students/index.babel')

module.exports = React.createClass({
	displayName: 'Main',

	propTypes: {
		app: React.PropTypes.string.isRequired,
	},

	getInitialState () {
		return {
			app: this.props.app,
		}
	},

	render () {
		return (
			<div>
				<Nav app={this.state.app} onNavClick={this.showApp} />
				{this.renderApp()}
			</div>
		)
	},

	renderApp () {
		switch (this.state.app) {
			case ('classes'):
				return <Classes />
			case ('students'):
				return <Students />
			default:
				return <Classes />
		}
	},

	showApp (app) {
		this.setState({ app })
	}
})
