var React = require('react')
var _ = require('underscore')

module.exports = React.createClass({
	displayName: 'ClassAttendance',

	propTypes: {
		attendance: React.PropTypes.array.isRequired,
		students: React.PropTypes.array.isRequired,
		lectures: React.PropTypes.array.isRequired,
		updateAttendance: React.PropTypes.func.isRequired,
	},

	render () {
		if (!this.props.attendance.length) return <h4>You dont' have any attendance records for this class yet.</h4>

		let lectureHeaders = _.map(this.props.lectures, lecture => {
			return <th key={lecture.id}>{lecture.name}</th>
		})

		let studentRows = _.map(this.props.students, student => {
			let studentId = student.id
			let records = _.chain(this.props.attendance)
				.filter(record => {
					if (studentId === record.class_student_id) return record
				})
				.map(record => {
					return (
						<td key={record.id}>
							<select className="form-control" defaultValue={record.did_attend} onChange={this.updateAttendance.bind(this, record.id)}>
								<option>Select</option>
								<option value={true}>Yes</option>
								<option value={false}>No</option>
							</select>
						</td>
					)
				})
				.value()

			return (
				<tr key={studentId}>
					<th>{student.first_name + ' ' + student.last_name}</th>
					{records}
				</tr>
			)
		})

		return (
			<table className="table table-bordered table-condensed table-striped">
				<thead>
					<tr>
						<th></th>
						{lectureHeaders}
					</tr>
				</thead>
				<tbody>
					{studentRows}
				</tbody>
			</table>
		)
	},

	updateAttendance (recordId, evt) {
		this.props.updateAttendance(recordId, evt.target.value)
	}
})
