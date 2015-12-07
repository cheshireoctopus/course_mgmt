var React = require('react')

module.exports = React.createClass({
	displayName: 'GitHubUserInfo',
	propTypes: {
		username: React.PropTypes.string,
		name: React.PropTypes.string,
		avatar: React.PropTypes.string,
	},
	render: function () {
		return (
			<div>
				<h2>{this.props.username}</h2>
				<h4>{this.props.name}</h4>
				<img src={this.props.avatar} />
			</div>
		)
	}
})
