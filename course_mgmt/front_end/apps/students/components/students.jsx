var _ = require('underscore')
var React = require('react')
var UserImage = require('components/user_image.jsx')
var utils = require('utils.babel')

module.exports = React.createClass({
	displayName: 'Students',

	propTypes: {
		onShowForm: React.PropTypes.func.isRequired,
		onShowStudent: React.PropTypes.func.isRequired,
		students: React.PropTypes.array.isRequired,
	},

	render () {
		let students = _.map(this.props.students, student => {
			return (
				<tr key={student.id} onClick={this.handleShowStudent.bind(this, student.id)}>
					<td className="text-center">
						<UserImage size={40} imgSrc={student.photo_url} />
					</td>
					<td>{student.first_name}</td>
					<td>{student.last_name}</td>
					<td><a onClick={e => {e.stopPropagation()}} href={utils.githubUserProfile(student.github_username)}>{student.github_username}</a></td>
					<td>{student.email}</td>
					<td>{student.classes.length && student.classes[0].name}</td>
				</tr>
			)
		})

		return (
			<div className="row">
				<div className="col-md-12 text-left">
					<button className="btn btn-primary" onClick={this.handleAddStudent}>Add Student</button>
					<hr />
				</div>
				<div className="col-md-12">
					{students && students.length ?
						<table className="table table-bordered table-condensed table-striped">
							<thead>
								<tr>
									<th></th>
									<th>First Name</th>
									<th>Last Name</th>
									<th>GitHub</th>
									<th>Email</th>
									<th>Class</th>
								</tr>
							</thead>
							<tbody>{students}</tbody>
						</table>
						: <h3>You haven't added any students yet</h3>}
				</div>
			</div>
		)
	},

	handleAddStudent () {
		this.props.onShowForm()
	},

	handleShowStudent (studentId) {
		this.props.onShowStudent(studentId)
	}
})
