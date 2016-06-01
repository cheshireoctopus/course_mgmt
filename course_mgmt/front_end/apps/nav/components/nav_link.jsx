var React = require('react')

module.exports = React.createClass({
	displayName: 'NavLink',

	propTypes: {
		title: React.PropTypes.string.isRequired,
		app: React.PropTypes.string.isRequired,
		onNavClick: React.PropTypes.func.isRequired,
		isActive: React.PropTypes.bool.isRequired,
	},

	render () {
		return <li onClick={this.handleClick} className={this.props.isActive ? 'active' : false}><a href="#">{this.props.title}</a></li>
	},

	handleClick () {
		return this.props.onNavClick(this.props.app)
	}
})
