var React = require('react')
var $ = require('jquery')
var _ = require('underscore')

var UserInfo = require('./user_info.jsx')
var ClassMembers = require('./class_members.jsx')

var TypeaheadResult = require('./typeahead/typeahead_result.jsx')

module.exports = React.createClass({
	displayName: 'UserSearch',

	getInitialState () {
	    return {
	    	loading: false,
	    	queryStatus: false,
	    	typeaheadResults: [],
	        userInfo: false,
	        classMembers: [],
	    };
	},

	render () {
		return (
			<div className="row">
				<div className="col-md-4">
					<h3>GitHub User Search</h3>
					<form onSubmit={this.userSearch} onKeyUp={this.userQuery}>
						<div className="form-group">
							<label className="control-label" htmlFor="username">GitHub User Name</label>
							<input className="form-control" ref="username" type="text" placeholder="GitHub User Name" name="username" />
							{this.state.typeaheadResults.length ? this.renderTypeaheadResults() : false}
						</div>
						<div className="form-group">
							<button className="btn btn-default" onClick={this.userSearch}>Search</button>
						</div>
					</form>
				</div>
				{this.state.userInfo ? this.renderUserInfo() : false}
				{this.state.classMembers.length ? this.renderClassMembers() : false}
			</div>
		)
	},

	renderUserInfo () {
		if (this.state.userInfo === 'Not Found') {
			return (
				<div className="col-md-4">
					<h2>Unable to locate user.</h2>
				</div>
			)
		}

		return (
			<div className="col-md-4">
				<UserInfo
					addMemberToClass={this.addMemberToClass}
					username={this.state.userInfo.username}
					name={this.state.userInfo.name}
					avatar={this.state.userInfo.avatar}
					html_url={this.state.userInfo.html_url}
				/>
			</div>
		)
	},

	renderClassMembers () {
		return (
			<ClassMembers members={this.state.classMembers} />
		)
	},

	userSearch (e) {
		e.preventDefault()
		// Todo - update this fn to use onInput
		var username = this.refs.username.value

		this.setState({ userInfo: false })

		$.get('/github/user/' + username)
			.done((data) => {
				this.buildUserInfo(data)
			})
			.fail((xhr) => {
				console.log('Error', xhr)
			})
	},

	buildUserInfo (data) {
		if (data.message === 'Not Found') return this.setState({ userInfo: 'Not Found'})

		var userInfo = {
			id: data.id,
			username: data.login,
			name: data.name,
			avatar: data.avatar_url,
			html_url: data.html_url,
		}

		return this.setState({userInfo})
	},

	addMemberToClass () {
		var currentClass = _.clone(this.state.classMembers)
		currentClass.push(this.state.userInfo)

		this.setState({ classMembers: currentClass })
	}
})
