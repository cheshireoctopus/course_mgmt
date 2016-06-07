var _ = require('underscore')
var React = require('react')

module.exports = React.createClass({
	displayName: 'Courses',

	propTypes: {
		courses: React.PropTypes.array.isRequired,
		showCourse: React.PropTypes.func.isRequired,
		toggleForm: React.PropTypes.func.isRequired,
	},

	render () {
		let courses = _.map(this.props.courses, c => {
			return (
				<a key={c.id} className="list-group-item" onClick={this.handleShowCourse.bind(this, c.id)}>{c.name}</a>
			)
		})

		return (
			<div className="row">
				<div className="col-md-12 text-left">
					<button className="btn btn-primary" onClick={this.handleAddCourse}>Add Course</button>
					<hr />
				</div>
				<div className="col-md-12">
					{courses && courses.length ? <ul className="list-group">{courses}</ul> : <h3>You haven't added any courses yet</h3>}
				</div>
			</div>
		)
	},

	handleAddCourse () {
		this.props.toggleForm()
	},

	handleShowCourse (courseId) {
		this.props.showCourse(courseId)
	}
})
