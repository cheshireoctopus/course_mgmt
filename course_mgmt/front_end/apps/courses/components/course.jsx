var React = require('react')
var _ = require('underscore')

module.exports = React.createClass({
	displayName: 'Course',

	propTypes: {
		classes: React.PropTypes.array.isRequired,
		homeworks: React.PropTypes.array.isRequired,
		id: React.PropTypes.number.isRequired,
		lectures: React.PropTypes.array.isRequired,
		name: React.PropTypes.string.isRequired,
		onDelete: React.PropTypes.func.isRequired,
		onEdit: React.PropTypes.func.isRequired,
		showCourses: React.PropTypes.func.isRequired,
	},

	render () {
		let classes = _.map(classes, classObj => {
			<a href="javascript:void(0)" key={classObj.id} className="list-group-item" onClick={this.props.showCourses}>{classObj.name}</a>
		})

		return (
			<div className="row">
				<div className="col-md-12">
					<a href="javascript:void(0)" onClick={this.props.showCourses}>Back to main</a>
					<h3>{this.props.name}</h3>
					<button onClick={this.handleOnEdit} className="btn btn-warning push-right">Edit</button>
					<button onClick={this.handleOnDelete} className="btn btn-danger">Delete</button>
					<hr />
				</div>
				<div className="col-md-12">
					<h4>Instances:</h4>
					{classes && classes.length ? <ul className="list-group">{classes}</ul> : <h3>No iterations of this course exist yet</h3>}
				</div>
			</div>
		)
	},

	handleOnDelete () {
		this.props.onDelete(this.props.id)
	},

	handleOnEdit () {
		this.props.onEdit(this.props.id)
	}
})
