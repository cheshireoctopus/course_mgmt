var _ = require('underscore')
var React = require('react')
var StudentRow = require('classes/components/student_row.jsx')
var DateTime = require('components/date_time.jsx')

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
		students: React.PropTypes.array,
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
				</div>
				<div className="col-md-4">
					<h4>Class Details</h4>
					<p>Start: <DateTime date={this.props.start_dt} /></p>
					<p>End: <DateTime date={this.props.end_dt} /></p>
					<p>Location: {this.props.location || 'N/A'}</p>
					<p>Student Count: {this.props.studentCount || 0}</p>
				</div>
				<div className="col-md-8">
					<h4>Students</h4>
					{this.props.students ? this.renderStudents() : false }
				</div>
			</div>
		)
	},

	renderStudents () {
		let students = _.map(this.props.students, student => <StudentRow key={student.id} {...student}/>)

		return (
			<ul className="list-group">
				{students}
			</ul>
		)
	},

	handleEdit () {
		this.props.onEdit(this.props.id)
	},

	handleDelete () {
		this.props.onDelete(this.props.id)
	},
})
