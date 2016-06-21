var $ = require('jquery')
var React = require('react')
var API = require('constants.js').API
var _ = require('underscore')

module.exports = React.createClass({
	displayName: 'ClassForm',

	propTypes: {
		classObj: React.PropTypes.object,
		courses: React.PropTypes.array.isRequired,
		onClose: React.PropTypes.func.isRequired,
		onSave: React.PropTypes.func.isRequired,
	},

	render () {
		let btnText = _.isEmpty(this.props.classObj) ? 'Create' : 'Save'
		let { name, start_dt, end_dt, course_id } = this.props.classObj
		let courseOptions = _.map(this.props.courses, course => <option value={course.id} key={course.id}>{course.name}</option>)

		if (courseOptions.length) {
			courseOptions.unshift(<option value="select" key={'select'}>Select Course</option>)
		} else {
			courseOptions.unshift(<option value="empty" key={'key'}>Classes must belong to a course</option>)
		}

		if (start_dt) start_dt = new Date(start_dt).toISOString().substring(0, 10)
		if (end_dt) end_dt = new Date(end_dt).toISOString().substring(0, 10)

		return (
			<div className="row">
				<div className="col-md-4">
					<h3>Create Class</h3>
					<div className="form-group">
						<label htmlFor="className" className="control-label">Class Name</label>
						<input ref="className" name="className" className="form-control" placeholder="Class Name" defaultValue={name} />
					</div>
					<div className="form-group">
						<label htmlFor="className" className="control-label">Course</label>
						<select ref="courseId" name="courseId" className="form-control" placeholder="Course Name" defaultValue={course_id} >
							{courseOptions}
						</select>
					</div>
					<div className="form-group">
						<label htmlFor="classStartDate" className="control-label">Class Start Date</label>
						<input ref="classStartDate" name="classStartDate" className="form-control" type="date" defaultValue={start_dt} />
					</div>
					<div className="form-group">
						<label htmlFor="classEndDate" className="control-label">Class End Date</label>
						<input ref="classEndDate" name="classEndDate" className="form-control" type="date" defaultValue={end_dt} />
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
		let newClassObj = _.clone(this.props.classObj)
		let classProperties = {
			name: this.refs.className.value,
			course_id: parseInt(this.refs.courseId.value),
			start_dt: new Date(this.refs.classStartDate.value).toJSON(),
			end_dt: new Date(this.refs.classEndDate.value).toJSON(),
		}

		_.extend(newClassObj, classProperties)

		return this.props.onSave(newClassObj)
	}
})
