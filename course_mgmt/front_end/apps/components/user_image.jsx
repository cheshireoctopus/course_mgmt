var React = require('react')

module.exports = React.createClass({
	displayName: 'UserImage',

	propTypes: {
		imgSrc: React.PropTypes.string.isRequired,
		size: React.PropTypes.number.isRequired,
	},

	render () {
		return <img height={this.props.size} width={this.props.size} src={this.props.imgSrc} />
	}
})
