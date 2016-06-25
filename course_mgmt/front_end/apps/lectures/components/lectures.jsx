var React = require('react')
var _ = require('underscore')

module.exports = React.createClass({
	displayName: 'Lectures',

	propTypes: {
		lectures: React.PropTypes.array.isRequired,
		onShowForm: React.PropTypes.func.isRequired,
		onShowLecture: React.PropTypes.func.isRequired,
	},

	render () {
		let lectureRows = _.map(this.props.lectures, lecture => {
			return (
				<tr key={lecture.id} onClick={this.handleShowLecture.bind(this, lecture.id)}>
					<td>{lecture.name}</td>
					<td>{lecture.description}</td>
				</tr>
			)
		})


		return (
			<div className="row">
				<div className="col-md-12 text-left">
					<button className="btn btn-primary" onClick={this.handleAddLecture}>Add Lecture</button>
					<hr />
				</div>
				<div className="col-md-12">
					{lectureRows && lectureRows.length ?
						<table className="table table-bordered table-condensed table-striped">
							<thead>
								<tr>
									<th>Lecture Name</th>
									<th>Description</th>
								</tr>
							</thead>
							<tbody>{lectureRows}</tbody>
						</table>
						: <h3>You haven't added any lectures yet</h3>}
				</div>
			</div>
		)
	},

	handleAddLecture () {
		this.props.onShowForm()
	},

	handleShowLecture (lectureId) {
		this.props.onShowLecture(lectureId)
	}
})
