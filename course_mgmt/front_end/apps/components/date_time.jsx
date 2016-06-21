var react = require('react')

module.exports = React.createClass({
	displayName: 'DateTime',

	propTypes: {
		date: React.PropTypes.string,
	},

	render () {
		let date = new Date(this.props.date).toLocaleDateString()

		return <span>{date}</span>
	}
})
