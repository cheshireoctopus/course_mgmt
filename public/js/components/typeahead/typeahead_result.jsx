var React = require('react')

module.exports = React.createClass({
	displayName: 'TypeaheadResult',

	propTypes: {
		username: React.PropTypes.string.isRequired,
		avatar: React.PropTypes.string.isRequired,
	},

	render () {
		return (
			<div className="clearfix">
				<div className="pull-left">
					<img src={this.props.avatar} />
				</div>
				<span>{this.props.username}</span>
			</div>
		)
	},
})
