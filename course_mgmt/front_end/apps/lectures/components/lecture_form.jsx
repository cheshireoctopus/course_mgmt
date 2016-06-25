var $ = require('jquery')
var React = require('react')
var API = require('constants.js').API
var _ = require('underscore')

module.exports = React.createClass({
	displayName: 'ClassForm',

	propTypes: {
		lecture: React.PropTypes.object,
		courses: React.PropTypes.array.isRequired,
		onClose: React.PropTypes.func.isRequired,
		onSave: React.PropTypes.func.isRequired,
	},

	render () {
		let btnText = _.isEmpty(this.props.lecture) ? 'Create' : 'Save'
		let { name, description, course_id } = this.props.lecture
		let courseOptions = _.map(this.props.courses, course => <option value={course.id} key={course.id}>{course.name}</option>)

		if (courseOptions.length) {
			courseOptions.unshift(<option value="select" key={'select'}>Select Course</option>)
		} else {
			courseOptions.unshift(<option value="empty" key={'key'}>Lectures must belong to a course</option>)
		}

		return (
			<div className="row">
				<div className="col-md-4">
					<h3>Create Lecture</h3>
					<div className="form-group">
						<label htmlFor="lectureName" className="control-label">Lecture Name</label>
						<input ref="lectureName" name="lectureName" className="form-control" placeholder="Lecture Name" defaultValue={name} />
					</div>
					<div className="form-group">
						<label htmlFor="description" className="control-label">Decription</label>
						<input ref="description" name="description" className="form-control" placeholder="First Name" defaultValue={description} />
					</div>
					<div className="form-group">
						<label htmlFor="courseId" className="control-label">Associated Course</label>
						<select ref="courseId" name="courseId" className="form-control" placeholder="Course Name">
							{courseOptions}
						</select>
					</div>
					<div className="form-group text-right">
						<button className="btn btn-primary push-right" onClick={this.handleFormSave}>{btnText}</button>
						<button className="btn btn-default" onClick={this.handleOnClose}>Cancel</button>
					</div>
				</div>
			</div>
		)
	},

	handleOnClose () {
		this.props.onClose()
	},

	handleFormSave () {
		let newLectureObj = _.clone(this.props.lecture)
		let stuentProps = {
			name: this.refs.lectureName.value,
			description: this.refs.description.value,
			course_id: parseInt(this.refs.courseId.value),
		}

		_.extend(newLectureObj, stuentProps)

		return this.props.onSave(newLectureObj)
	}
})
