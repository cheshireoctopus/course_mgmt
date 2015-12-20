var React = require('react')

var UserInfo = require('./user_info.jsx')
var UserSearch = require('./user_search.jsx')

module.exports = React.createClass({
	displayName: 'App',

	render: function () {
		return (
			<UserSearch />
		)
	}
})
