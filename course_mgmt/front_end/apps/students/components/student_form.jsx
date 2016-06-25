var $ = require('jquery')
var React = require('react')
var API = require('constants.js').API
var _ = require('underscore')

module.exports = React.createClass({
	displayName: 'ClassForm',

	propTypes: {
		student: React.PropTypes.object,
		classes: React.PropTypes.array.isRequired,
		onClose: React.PropTypes.func.isRequired,
		onSave: React.PropTypes.func.isRequired,
	},

	render () {
		let btnText = _.isEmpty(this.props.student) ? 'Create' : 'Save'
		let { first_name, last_name, github_username, email, photo_url } = this.props.student
		let classOptions = _.map(this.props.classes, c => <option value={c.id} key={c.id}>{c.name}</option>)

		if (classOptions.length) {
			classOptions.unshift(<option value="select" key={'select'}>Select Class</option>)
		} else {
			classOptions.unshift(<option value="empty" key={'key'}>Students must belong to a class</option>)
		}

		return (
			<div className="row">
				<div className="col-md-4">
					<h3>Create Student</h3>
					<div className="form-group">
						<label htmlFor="photoURL" className="control-label">Picture</label>
						<input ref="photoURL" name="photoURL" className="form-control" placeholder="http://..." defaultValue={photo_url} />
					</div>
					<div className="form-group">
						<label htmlFor="firstName" className="control-label">First Name</label>
						<input ref="firstName" name="firstName" className="form-control" placeholder="First Name" defaultValue={first_name} />
					</div>
					<div className="form-group">
						<label htmlFor="lastName" className="control-label">Last Name</label>
						<input ref="lastName" name="lastName" className="form-control" placeholder="Last Name" defaultValue={last_name} />
					</div>
										<div className="form-group">
						<label htmlFor="githubUsername" className="control-label">GitHub Username</label>
						<input ref="githubUsername" name="githubUsername" className="form-control" placeholder="GitHub Username" defaultValue={github_username} />
					</div>
					<div className="form-group">
						<label htmlFor="email" className="control-label">Email</label>
						<input ref="email" name="email" className="form-control" placeholder="Email" defaultValue={email} />
					</div>
					<div className="form-group">
						<label htmlFor="classId" className="control-label">Associated Class</label>
						<select ref="classId" name="classId" className="form-control" placeholder="Course Name">
							{classOptions}
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
		let newStudentObj = _.clone(this.props.student)
		let stuentProps = {
			photo_url: this.refs.photoURL.value,
			first_name: this.refs.firstName.value,
			last_name: this.refs.lastName.value,
			github_username: this.refs.githubUsername.value,
			email: this.refs.email.value,
			class_id: parseInt(this.refs.classId.value),
		}

		_.extend(newStudentObj, stuentProps)

		return this.props.onSave(newStudentObj)
	}
})
