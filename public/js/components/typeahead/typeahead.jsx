var React = require('react')

module.exports = React.createClass({
	displayName: 'Typeahead',

	propTypes: {
	},

	getInitialState () {
		return {
			results: []
		}
	},

	render () {
		return (
			<div className="form-group">
				<label className="control-label" htmlFor="username">Github Username</label>
				<input
					className="form-control"
					ref="username"
					name="username"
					placeholder={this.props.placeholder}
					onKeyUp={this.userQuery}
				/>
				{this.state.results.length ? this.renderResults() : false}
			</div>
		)
	},

	renderResults () {
		console.log('should be renderTypeaheadResults')
		return this.state.typeaheadResults.map((res) => {
			return (
				<TypeaheadResult key={_.uniqueId()} username={res.username} avatar={res.avatar} />
			)
		})
	},

	userQuery () {
		var query = this.refs.typeahead-input.value

		// don't hit github api unless query is 3 letters in length
		if (query.length <= 2) return

		$.get('/github/search/users/' + query)
			.done((data) => {
				this.processUserQuery(data)
			})
			.fail((xhr) => {
				console.log(xhr)
			})
	},

	processUserQuery (data) {
		// if (!data || !data.items || !data.items.length) return this.setState({ queryStatus: false })

		// only show first 10 results
		var results = []
		for (var i = 0, l = data.items.length; i < 10; i++) {
			var res = data.items[i]
			console.log(res)
			results.push({
				username: res.login || false,
				avatar: res.avatar_url || false,
			})
		}

		this.setState({
			typeaheadResults: results,
		})
	},

})
