var _ = require('underscore')
var React = require('react')

module.exports = React.createClass({
	displayName: 'Courses',

	propTypes: {
		courses: React.PropTypes.object.isRequired,
		showCourse: React.PropTypes.func.isRequired,
		toggleForm: React.PropTypes.func.isRequired,
	},

	render () {


		return (
			<div className="row">
				<div className="col-md-12 text-left">
					<button className="btn btn-primary" onClick={this.handleAddCourse}>Add Course</button>
					<hr />
				</div>
				<div className="col-md-12">
					{_.isEmpty(this.props.courses) ? <h3>You haven't added any courses yet</h3> : this.renderCourses()}
				</div>
			</div>
		)
	},

	renderCourses () {
		let courses = this.props.courses.map(course => {
			return (
				<a key={course.get('id')} className="list-group-item" onClick={this.handleShowCourse.bind(this, course.get('id'))}>{course.get('name')}</a>
			)
		})

		return <ul className="list-group">{courses}</ul>
	},

	handleAddCourse () {
		this.props.toggleForm()
	},

	handleShowCourse (courseId) {
		this.props.showCourse(courseId)
	}
})
