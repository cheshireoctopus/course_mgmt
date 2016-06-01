var _ = require('underscore')
var React = require('react')

module.exports = React.createClass({
	displayName: 'Classes',

	propTypes: {
		classes: React.PropTypes.array.isRequired,
	},

	render () {
		let classes = _.map(this.props.classes, c => {
			return (
				<a key={c.id} className="list-group-item" onClick={this.handleClick.bind(this, c.id)}>{c.name}</a>
			)
		})

		return (
			<div className="row">
				<div className="col-md-12">
					{classes && classes.length ? <ul className="list-group">{classes}</ul> : <h3>No Classes Exist Yet</h3>}
				</div>
			</div>
		)
	},

	handleClick (classId) {
		this.props.showClass(classId)
	}
})
