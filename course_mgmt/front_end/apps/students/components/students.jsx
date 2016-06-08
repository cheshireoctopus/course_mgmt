var _ = require('underscore')
var React = require('react')
var StudentRow = require('students/components/student_row.jsx')

module.exports = React.createClass({
	displayName: 'Students',

	propTypes: {
		showStudent: React.PropTypes.func.isRequired,
		students: React.PropTypes.array.isRequired,
	},

	render () {
		let students = _.map(this.props.students, student => <StudentRow key={student.id} {...student} />)

		return (
			<div className="row">
				<div className="col-md-12">
					<ul className="list-group">
						{students && students.length ? students : <h3>You haven't added any students yet</h3>}
					</ul>
				</div>
			</div>
		)
	},
})
