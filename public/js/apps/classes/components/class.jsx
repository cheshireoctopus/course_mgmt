var _ = require('underscore')
var React = require('react')
var StudentRow = require('./student_row.jsx')

module.exports = React.createClass({
	displayName: 'Class',

	propTypes: {
		description: React.PropTypes.string,
		end: React.PropTypes.string,
		id: React.PropTypes.string.isRequired,
		location: React.PropTypes.string,
		name: React.PropTypes.string,
		start: React.PropTypes.string,
		studentCount: React.PropTypes.number,
		students: React.PropTypes.array,
		showClasses: React.PropTypes.func.isRequired
	},

	render () {
		return (
			<div className="row">
				<div className="col-md-12">
					<a onClick={this.props.showClasses}>Back to Main</a>
				</div>
				<div className="col-md-12">
					<h2>{this.props.name}</h2>
				</div>
				<div className="col-md-4">
					<h4>Class Details</h4>
					<p>Start: {this.props.start}</p>
					<p>End: {this.props.end}</p>
					<p>Location: {this.props.location}</p>
					<p>Student Count: {this.props.studentCount}</p>
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
})
