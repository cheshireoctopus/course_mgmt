var React = require('react')
var Class = require('./class.jsx')
var Classes = require('./classes.jsx')

module.exports = React.createClass({
	displayName: 'ClassesController',

	propTypes: {
		class: React.PropTypes.oneOfType([
			React.PropTypes.bool.isRequired,
			React.PropTypes.object.isRequired,
		]),
		classes: React.PropTypes.array.isRequired,
		isLoading: React.PropTypes.bool.isRequired,
		showClass: React.PropTypes.func.isRequired,
	},

	render () {
		return (
			<div>
				<h1>Classes</h1>
				<hr />
				{this.isLoading ? <h3>Loading...</h3> : this.renderView()}
			</div>
		)
	},

	renderView () {
		if (this.props.class) return <Class {...this.props.class} />
		return <Classes classes={this.props.classes} showClass={this.props.showClass} />
	}
})
