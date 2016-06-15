var $ = require('jquery')
var React = require('react')
var API = require('constants.js').API

module.exports = React.createClass({
	displayName: 'CourseForm',

	propTypes: {
		course: React.PropTypes.object,
		onClose: React.PropTypes.func.isRequired,
		onSave: React.PropTypes.func.isRequired,
		onEdit: React.PropTypes.func.isRequired,
	},

	getInitialState () {
		return {
			isLoading: false,
		}
	},

	componentDidMount () {
		if (!_.isEmpty(this.props.course)) this.refs.courseName.value = this.props.course.get('name')
	},

	render () {
		let btnText = _.isEmpty(this.props.course) ? 'Create' : 'Save'

		return (
			<div className="row">
				<div className="col-md-4">
					{this.state.isLoading ? <h3>Loading...</h3> :
						<div>
							<h3>Create Course</h3>
							<div className="form-group">
								<label htmlFor="courseName" className="control-label">Course Name</label>
								<input ref="courseName" name="courseName" className="form-control" placeholder="Course Name" />
							</div>
							<div className="form-group text-right">
								<button className="btn btn-primary" onClick={this.handleFormSave}>{btnText}</button>
								<button className="btn btn-default" onClick={this.handleOnClose}>Cancel</button>
							</div>
						</div>
					}
				</div>
			</div>
		)
	},

	handleOnClose () {
		this.props.onClose(this.props.course.id)
	},

	handleFormSave () {
		this.setState({ isLoading: true })

		let courseName = this.refs.courseName.value

		if (_.isEmpty(this.props.course)) return this.props.onSave(courseName)

		return this.props.onEdit(this.props.course.id, courseName)
	}
})
