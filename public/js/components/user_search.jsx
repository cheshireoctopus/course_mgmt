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
			<div className="row">
				<div className="col-md-4">
					<h3>GitHub User Search</h3>
					<form onSubmit={this.userSearch}>
						<div className="form-group">
							<label className="control-label" htmlFor="username">GitHub User Name</label>
							<input className="form-control" ref="username" type="text" placeholder="GitHub User Name" name="username" />
						</div>
						<div className="form-group">
							<button className="btn btn-default" onClick={this.userSearch}>Search</button>
						</div>
					</form>
				</div>
				{this.state.userInfo ? this.renderUserInfo() : false}
			</div>
		)
	},

	renderUserInfo: function () {
		if (this.state.userInfo === 'Not Found') {
			return (
				<div className="col-md-4">
					<h2>Unable to locate user.</h2>
				</div>
			)
		}

		return (
			<div className="col-md-4">
				<UserInfo {...this.state.userInfo}/>
			</div>
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
