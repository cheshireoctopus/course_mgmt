var $ = require('jquery')
var React = require('react')
var API = require('./../../constants.js').API

module.exports = React.createClass({
	displayName: 'CourseForm',

	propTypes: {
		onClose: React.PropTypes.func.isRequired,
		onSave: React.PropTypes.func.isRequired,
	},

	getInitialState () {
		return {
			isLoading: false,
		}
	},

	render () {
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
								<button className="btn btn-primary" onClick={this.handleFormSave}>Create</button>
								<button className="btn btn-default" onClick={this.props.onClose}>Cancel</button>
							</div>
						</div>
					}
				</div>
			</div>
		)
	},

	handleFormSave () {
		this.setState({ isLoading: true })

		let courseName = this.refs.courseName.value

		this.props.onSave(courseName)
	}
})
