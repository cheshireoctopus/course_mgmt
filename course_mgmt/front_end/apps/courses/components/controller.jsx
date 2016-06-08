var React = require('react')
var Course = require('courses/components/course.jsx')
var Courses = require('courses/components/courses.jsx')
var CourseForm = require('courses/components/course_form.jsx')

module.exports = React.createClass({
	displayName: 'CoursesController',

	propTypes: {
		course: React.PropTypes.object.isRequired,
		courseClasses: React.PropTypes.array.isRequired,
		courses: React.PropTypes.array.isRequired,
		deleteCourse: React.PropTypes.func.isRequired,
		isLoading: React.PropTypes.bool.isRequired,
		isShowingCourse: React.PropTypes.bool.isRequired,
		isShowingForm: React.PropTypes.bool.isRequired,
		saveForm: React.PropTypes.func.isRequired,
		showCourse: React.PropTypes.func.isRequired,
		showCourses: React.PropTypes.func.isRequired,
		toggleForm: React.PropTypes.func.isRequired,
	},

	render () {
		return (
			<div className="container">
				<div className="row">
					<div className="col-md-12">
						<h1>Courses</h1>
						<hr />
					</div>
				</div>
				{this.props.isShowingForm ? this.renderForm() : this.renderMain()}
			</div>
		)
	},

	renderMain () {
		if (this.props.isLoading) return <h3>Loading...</h3>
		if (this.props.isShowingCourse)
			return <Course
						{...this.props.course}
						classes={this.props.courseClasses}
						onDelete={this.props.deleteCourse}
						onEdit={this.props.toggleForm}
						showCourses={this.props.showCourses}
					/>

		return <Courses courses={this.props.courses} showCourse={this.props.showCourse} toggleForm={this.props.toggleForm} />
	},

	renderForm () {
		return <CourseForm course={this.props.course} onSave={this.props.saveForm} onClose={this.props.toggleForm} />
	}
})
