var $ = require('jquery')
var React = require('react')
var ReactDOM = require('react-dom')

var GitHubUserInfo = require('./components/user_info.jsx')

$('#github-user').submit(function (e) {
	e.preventDefault()
	var userName = $(this).find('input[name]').val()

	$.get('/github/user/' + userName)
		.done(function (res) {
			renderUserInfo(res)
		})
		.fail(function (res) {
			console.log('fail ', res)
		})
})

function renderUserInfo (data) {
	var el = $('#github-user-info')[0]
	var props = {
		username: data.login,
		name: data.name,
		avatar: data.avatar_url,
	}
	var gitHubUserInfo = React.createElement(GitHubUserInfo, props)
	ReactDOM.render(gitHubUserInfo, el)
}
