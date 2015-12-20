var React = require('react')
var _ = require('underscore')

module.exports = React.createClass({
	displayName: 'ClassMembers',

	propTypes: {
		members: React.PropTypes.array.isRequired,
	},

	render: function () {
		var members = _.map(this.props.members, function (member) {
			return (
				<div className="clearfix" key={member.id}>
					<div className="pull-left">
						<img src={member.avatar} />
					</div>
					<div className="pull-right">
						<h4>{member.username}</h4>
						<p>{member.name}</p>
					</div>
				</div>
			)
		})

		return (
			<div>
				<h2>Current Class</h2>
				<hr/>
				{members}
			</div>
		)
	}
})
