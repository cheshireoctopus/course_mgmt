var React = require('react')
var $ = require('jquery')

module.exports = React.createClass({
	displayName: 'Landing',

	render: function () {
		return (
			<div className="row">
				<h1 className="text-center">FEWD MGMT</h1>

				<div className="col-md-6 col-md-offset-3">
					<form>
						<div className="form-group">
							<label htmlFor="username" className="control-label">GitHub Username</label>
							<input type="text" ref="username" id="username" className="form-control" placeholder="GitHub Username"/>
						</div>
						<button onClick={this.authUser} className="btn btn-default">Sign up</button>
					</form>
				</div>
			</div>
		)
	},

	authUser: function (e) {
		e.preventDefault()
		var username = this.refs.username.value

		$.get('/github/auth/' + username)
			.done(function (res) {
				console.log(res)
			})
			.fail(function (xhr) {
				console.log(xhr)
			})
	}
})
