var _ = require('underscore')
var React = require('react')
var DateTime = require('components/date_time.jsx')

module.exports = React.createClass({
	displayName: 'Classes',

	propTypes: {
		classes: React.PropTypes.array.isRequired,
		showClass: React.PropTypes.func.isRequired,
		onShowForm: React.PropTypes.func.isRequired,
	},

	render () {
		let classes = _.map(this.props.classes, c => {
			return (
				<tr key={c.id} onClick={this.handleShowClass.bind(this, c.id)}>
					<td>{c.name}</td>
					<td>{c.course_id}</td>
					<td><DateTime date={c.start_dt} /></td>
					<td><DateTime date={c.end_dt} /></td>
				</tr>
			)
		})

		return (
			<div className="row">
				<div className="col-md-12 text-left">
					<button className="btn btn-primary" onClick={this.handleAddClass}>Add Class</button>
					<hr />
				</div>
				<div className="col-md-12">

					{classes && classes.length ?
						<table className="table table-bordered table-condensed table-striped">
							<thead>
								<tr>
									<th>Class Name</th>
									<th>Course</th>
									<th>Start Date</th>
									<th>End Date</th>
								</tr>
							</thead>
							<tbody>{classes}</tbody>
						</table>
						: <h3>You haven't added any classes yet</h3>}
				</div>
			</div>
		)
	},

	handleAddClass () {
		this.props.onShowForm()
	},

	handleShowClass (classId) {
		this.props.showClass(classId)
	}
})
