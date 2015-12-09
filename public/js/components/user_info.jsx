var React = require('react')
var _ = require('underscore')
var $ = require('jquery')

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
		console.log('component did mount')
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
		if (!this.state.repos.length) return this.renderEmptyRepos()

		return _.map(this.state.repos, function (repo) {
			return (
				<div key={repo.id}>
					<a href={repo.html_url}><h5>{repo.name}</h5></a>
					<p>Last Updated: {repo.updated_at}</p>
				</div>
			)
		})
	},

	renderRepoLoad: function () {
		return (
			<p>Loading repositories...</p>
		)
	},

	renderEmptyRepos: function () {
		return (
			<p>Unable to locate any associated repositories</p>
		)
	},
})
