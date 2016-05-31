var React = require('react')
var Student = require('./student.jsx')
var Students = require('./students.jsx')

module.exports = React.createClass({
	displayName: 'StudentsController',

	propTypes: {
		student: React.PropTypes.object.isRequired,
		students: React.PropTypes.array.isRequired,
		isLoading: React.PropTypes.bool.isRequired,
		isShowingStudent: React.PropTypes.bool.isRequired,
		showStudent: React.PropTypes.func.isRequired,
		showStudents: React.PropTypes.func.isRequired,
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
				{this.isLoading ? <h3>Loading...</h3> : this.renderView()}
			</div>
		)
	},

	renderView () {
		if (this.props.isShowingStudent) return <Student {...this.props.student} showStudents={this.props.showStudents} />
		return <Students students={this.props.students} showStudent={this.props.showStudent} />
	}
})
