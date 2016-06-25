var React = require('react')
var UserImage = require('components/user_image.jsx')
var utils = require('utils.babel')

module.exports = React.createClass({
	displayName: 'Student',

	propTypes: {
		id: React.PropTypes.number.isRequired,
		first_name: React.PropTypes.string.isRequired,
		last_name: React.PropTypes.string.isRequired,
		github_username: React.PropTypes.string.isRequired,
		email: React.PropTypes.string.isRequired,
		photo_url: React.PropTypes.string.isRequired,
		assignments: React.PropTypes.array.isRequired,
		attendances: React.PropTypes.array.isRequired,
		classes: React.PropTypes.array.isRequired,
		onShowStudents: React.PropTypes.func.isRequired,
		onEdit: React.PropTypes.func.isRequired,
		onDelete: React.PropTypes.func.isRequired,
	},

	render () {
		return (
			<div className="row">
				<div className="col-md-12">
					<a href="javascript:void(0)" onClick={this.props.onShowStudents}>Back to Main</a>
				</div>
				<div className="row">
					<div className="col-md-12">
						<h2>{this.props.first_name} {this.props.last_name}</h2>
						<UserImage size={80} imgSrc={this.props.photo_url} />
						<button className="btn btn-warning push-right" onClick={this.handleEdit}>Edit</button>
						<button className="btn btn-danger" onClick={this.handleDelete}>Delete</button>
						<hr/>
					</div>
				</div>
				<div className="row">
					<div className="col-md-4">
						<h4>Student Details</h4>
						<p><strong>Email:</strong> {this.props.email}</p>
						<p><strong>Github:</strong> <a href={utils.githubUserProfile(this.props.github_username)}>{this.props.github_username}</a></p>
					</div>
				</div>
			</div>
		)
	},

	handleEdit () {
		this.props.onEdit(this.props.id)
	},

	handleDelete () {
		this.props.onDelete(this.props.id)
	},
})
