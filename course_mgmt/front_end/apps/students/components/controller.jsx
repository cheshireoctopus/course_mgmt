var React = require('react')
var Student = require('students/components/student.jsx')
var Students = require('students/components/students.jsx')
var Form = require('students/components/student_form.jsx')

module.exports = React.createClass({
	displayName: 'StudentsController',

	propTypes: {
		classes: React.PropTypes.array.isRequired,
		student: React.PropTypes.object.isRequired,
		students: React.PropTypes.array.isRequired,
		isLoading: React.PropTypes.bool.isRequired,
		isShowingStudent: React.PropTypes.bool.isRequired,
		isShowingForm: React.PropTypes.bool.isRequired,
		onSaveForm: React.PropTypes.func.isRequired,
		onShowForm: React.PropTypes.func.isRequired,
		onShowStudent: React.PropTypes.func.isRequired,
		onShowStudents: React.PropTypes.func.isRequired,
		onEditStudent: React.PropTypes.func.isRequired,
		onDeleteStudent: React.PropTypes.func.isRequired,
	},

	render () {
		return (
			<div className="container">
				<div className="row">
					<div className="col-md-12">
						<h1>Students</h1>
						<hr />
					</div>
				</div>
				{this.props.isShowingForm ? this.renderForm() : this.renderStudents()}
			</div>
		)
	},

	renderStudents () {
		if (this.props.isLoading) return <h3>Loading...</h3>
		if (this.props.isShowingStudent) {
			return <Student
						{...this.props.student}
						onShowStudents={this.props.onShowStudents}
						onEdit={this.props.onEditStudent}
						onDelete={this.props.onDeleteStudent}
					/>
		}

		return <Students
					students={this.props.students}
					onShowStudent={this.props.onShowStudent}
					onShowForm={this.props.onShowForm}
				/>
	},

	renderForm () {
		return <Form
					student={this.props.student}
					classes={this.props.classes}
					onSave={this.props.onSaveForm}
					onClose={this.props.onShowStudents}
				/>
	}
})
