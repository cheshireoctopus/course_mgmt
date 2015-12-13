var React = require('react')
var _ = require('underscore')
var $ = require('jquery')

var Repos = require('./repos.jsx')

module.exports = React.createClass({
	displayName: 'UserInfo',

	propTypes: {
		username: React.PropTypes.string.isRequired,
		name: React.PropTypes.string.isRequired,
		avatar: React.PropTypes.string.isRequired,
		html_url: React.PropTypes.string.isRequired,
	},

	getInitialState() {
	    return {
	        repos: false,
	    };
	},

	componentDidMount() {
		$.get('github/repos/' + this.props.username)
			.done(function (data) {
				if (this.isMounted()) this.setState({ repos: data })
			}.bind(this))
			.fail(function (xhr) {
				console.log('Error', xhr)
			})
	},

	render: function () {
		return (
			<div>
				<a href={this.props.html_url} target="_blank"><h2>{this.props.username}</h2></a>
				<h4>{this.props.name}</h4>
				<img src={this.props.avatar} />
				<h3>Repositories</h3>
				{this.state.repos ? this.renderRepos() : this.renderRepoLoad()}
			</div>
		)
	},

	renderRepos: function () {
		return (
			<Repos repos={this.state.repos} />
		)
	},

	renderRepoLoad: function () {
		return (
			<p>Loading repositories...</p>
		)
	},
})
