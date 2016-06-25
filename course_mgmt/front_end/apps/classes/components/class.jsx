var _ = require('underscore')
var React = require('react')
var DateTime = require('components/date_time.jsx')
var UserImage = require('components/user_image.jsx')
var utils = require('utils.babel')

module.exports = React.createClass({
	displayName: 'Class',

	propTypes: {
		description: React.PropTypes.string,
		end_dt: React.PropTypes.string,
		id: React.PropTypes.number.isRequired,
		location: React.PropTypes.string,
		name: React.PropTypes.string,
		start_dt: React.PropTypes.string,
		studentCount: React.PropTypes.number,
		students: React.PropTypes.array.isRequired,
		showClasses: React.PropTypes.func.isRequired,
		onEdit: React.PropTypes.func.isRequired,
		onDelete: React.PropTypes.func.isRequired
	},

	render () {
		return (
			<div className="row">
				<div className="col-md-12">
					<a onClick={this.props.showClasses}>Back to Main</a>
				</div>
				<div className="col-md-12">
					<h2>{this.props.name}</h2>
					<button className="btn btn-warning push-right" onClick={this.handleEdit}>Edit</button>
					<button className="btn btn-danger" onClick={this.handleDelete}>Delete</button>
					<hr/>
				</div>
				<div className="col-md-2">
					<h4>Class Details</h4>
					<p>Start: <DateTime date={this.props.start_dt} /></p>
					<p>End: <DateTime date={this.props.end_dt} /></p>
					<p>Location: {this.props.location || 'N/A'}</p>
					<p>Student Count: {this.props.studentCount || 0}</p>
				</div>
				<div className="col-md-10">
					<h4>Students</h4>
					{this.props.students && this.props.students.length ? this.renderStudents() : <p>You haven't added any students to this class yet.</p> }
				</div>
			</div>
		)
	},

	renderStudents () {
		let students = _.map(this.props.students, student => {
			return (
				<tr key={student.id}>
					<td className="text-center">
						<UserImage size={40} imgSrc={student.photo_url} />
					</td>
					<td>{student.first_name}</td>
					<td>{student.last_name}</td>
					<td><a onClick={e => {e.stopPropagation()}} href={utils.githubUserProfile(student.github_username)}>{student.github_username}</a></td>
					<td>{student.email}</td>
				</tr>
			)
		})

		return (
			<table className="table table-bordered table-condensed table-striped">
				<thead>
					<tr>
						<th></th>
						<th>First Name</th>
						<th>Last Name</th>
						<th>GitHub</th>
						<th>Email</th>
					</tr>
				</thead>
				<tbody>{students}</tbody>
			</table>
		)
	},

	handleEdit () {
		this.props.onEdit(this.props.id)
	},

	handleDelete () {
		this.props.onDelete(this.props.id)
	},
})
