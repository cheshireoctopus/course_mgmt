var React = require('react')
var _ = require('underscore')

module.exports = React.createClass({
	displayName: 'Repositories',

	propTypes: {
		repos: React.PropTypes.array,
	},

	getInitialState: function () {
	    return {
	        showAll: false
	    };
	},

	render: function () {
		return (
			<div>{this.renderRepoContainer()}</div>
		)
	},

	renderRepoContainer: function () {
		if (!this.props.repos.length) return this.renderEmptyRepos()
		var buttonText = this.state.showAll ? 'Hide' : 'Show'

		return (
			<div>
				<p>
					{this.props.repos.length} repositories found.
					<button className="btn btn-default" onClick={this.toggleShowAll}>{buttonText}</button>
				</p>
				{this.state.showAll ? this.renderRepos() : false}
			</div>
		)
	},

	renderRepos: function () {
		return _.map(this.props.repos, function (repo) {
			return (
				<div key={repo.id}>
					<a href={repo.html_url}><h5>{repo.name}</h5></a>
					<p>Last Updated: {repo.updated_at}</p>
				</div>
			)
		})
	},

	renderEmptyRepos: function () {
		return (
			<p>Unable to locate any associated repositories.</p>
		)
	},

	toggleShowAll: function () {
		this.setState({
			showAll: !this.state.showAll
		})
	}
})
