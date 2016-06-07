var _ = require('underscore')
var React = require('react')

module.exports = React.createClass({
	displayName: 'Classes',

	propTypes: {
		classes: React.PropTypes.array.isRequired,
		showClass: React.PropTypes.func.isRequired,
		showForm: React.PropTypes.func.isRequired,
	},

	render () {
		let classes = _.map(this.props.classes, c => {
			return (
				<a key={c.id} className="list-group-item" onClick={this.handleShowClass.bind(this, c.id)}>{c.name}</a>
			)
		})

		return (
			<div className="row">
				<div className="col-md-12 text-left">
					<button className="btn btn-primary" onClick={this.handleAddClass}>Add Class</button>
					<hr />
				</div>
				<div className="col-md-12">
					{classes && classes.length ? <ul className="list-group">{classes}</ul> : <h3>You haven't added any classes yet</h3>}
				</div>
			</div>
		)
	},

	handleAddClass () {
		this.props.showForm()
	},

	handleShowClass (classId) {
		this.props.showClass(classId)
	}
})
