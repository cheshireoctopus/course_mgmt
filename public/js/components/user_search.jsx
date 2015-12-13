var React = require('react')
var $ = require('jquery')

var UserInfo = require('./user_info.jsx')

module.exports = React.createClass({
	displayName: 'UserSearch',

	getInitialState() {
	    return {
	        userInfo: false,
	    };
	},

	render: function () {
		return (
			<div>
				<h3>GitHub User Search</h3>
				<form onSubmit={this.userSearch}>
					<label htmlFor="username">GitHub User Name</label>
					<input ref="username" type="text" placeholder="GitHub User Name" name="username" />
					<button onClick={this.userSearch}>Search</button>
				</form>
				<hr />
				{this.state.userInfo ? this.renderUserInfo() : false}
			</div>
		)
	},

	renderUserInfo: function () {
		if (this.state.userInfo === 'Not Found') {
			return (
				<div className="row">
					<h2>Unable to locate user.</h2>
				</div>
			)
		}

		return (
			<UserInfo {...this.state.userInfo}/>
		)
	},

	userSearch: function (e) {
		e.preventDefault()
		// Todo - update this fn to use onInput
		var username = this.refs.username.value

		this.setState({ userInfo: false })

		$.get('/github/user/' + username)
			.done(function (data) {
				this.buildUserInfo(data)
			}.bind(this))
			.fail(function (xhr) {
				console.log('Error', xhr)
			})
	},

	buildUserInfo: function (data) {
		if (data.message === 'Not Found') return this.setState({ userInfo: 'Not Found'})

		var userInfo = {
			username: data.login,
			name: data.name,
			avatar: data.avatar_url,
			html_url: data.html_url,
		}

		return this.setState({userInfo})
	}
})
