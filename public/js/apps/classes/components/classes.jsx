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
			<ul className="list-group">
				{classes}
			</ul>
		)
	},

	handleClick (classId) {
		this.props.showClass(classId)
	}
})
