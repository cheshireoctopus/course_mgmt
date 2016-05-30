var React = require('react')

module.exports = React.createClass({
	displayName: 'StudentRow',

	propTypes: {
		id: React.PropTypes.string.isRequired,
		name: React.PropTypes.string.isRequired,
		email: React.PropTypes.string.isRequired,
		github: React.PropTypes.string.isRequired,
		photo_url: React.PropTypes.string.isRequired,
	},

	render () {
		return (
			<a className="list-group-item" onClick={this.handleClick}>{this.props.name}</a>
		)
	},

	handleClick () {

	}
})
