var React = require('react')
var _ = require('underscore')

module.exports = React.createClass({
	displayName: 'Lecture',

	propTypes: {
		id: React.PropTypes.number.isRequired,
		name: React.PropTypes.string.isRequired,
		description: React.PropTypes.string.isRequired,
		classes: React.PropTypes.array.isRequired,
		courses: React.PropTypes.array.isRequired,
		onShowLectures: React.PropTypes.func.isRequired,
		onDeleteLecture: React.PropTypes.func.isRequired,
	},

	render () {
		return (
			<div className="row">
				<div className="col-md-12">
					<a href="javascript:void(0)" onClick={this.props.onShowLectures}>Back to Main</a>
				</div>
				<div className="col-md-12">
					<h2>{this.props.name}</h2>
					<p>{this.props.description}</p>
					<button className="btn btn-danger" onClick={this.handleOnDelete}>Delete Lecture</button>
					<hr />
				</div>
				<div className="col-md-6">
					<h3>Courses</h3>
					{this.props.courses && this.props.courses.length ? this.renderCourses() : <p>This lecture does not belong to any courses.</p>}
				</div>
				<div className="col-md-6">
					<h3>Classes</h3>
					{this.props.classes && this.props.classes.length ? this.renderClasses() : <p>This lecture does not belong to any classes.</p>}
				</div>
			</div>
		)
	},

	renderCourses () {
		let courses = _.map(this.props.courses, course => {
			return (
				<tr key={course.id}>
					<td>{course.name}</td>
				</tr>
			)
		})

		return (
			<table className="table table-bordered table-condensed table-striped">
				<thead>
					<tr>
						<td>Course Name</td>
					</tr>
				</thead>
				<tbody>{courses}</tbody>
			</table>
		)
	},

	renderClasses () {
		return <p>Some classes should be here</p>
	},

	handleOnDelete () {
		return this.props.onDeleteLecture(this.props.id)
	}
})
