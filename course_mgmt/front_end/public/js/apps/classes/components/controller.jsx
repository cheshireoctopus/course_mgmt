var React = require('react')
var Class = require('./class.jsx')
var Classes = require('./classes.jsx')

module.exports = React.createClass({
	displayName: 'ClassesController',

	propTypes: {
		class: React.PropTypes.oneOfType([
			React.PropTypes.bool.isRequired,
			React.PropTypes.object.isRequired,
		]),
		classes: React.PropTypes.array.isRequired,
		isLoading: React.PropTypes.bool.isRequired,
		isShowingClass: React.PropTypes.bool.isRequired,
		showClass: React.PropTypes.func.isRequired,
		showClasses: React.PropTypes.func.isRequired,
		studentsByClass: React.PropTypes.array.isRequired,
	},

	render () {
		return (
			<div className="container">
				<div className="row">
					<div className="col-md-12">
						<h1>Classes</h1>
						<hr />
					</div>
				</div>
				{this.isLoading ? <h3>Loading...</h3> : this.renderView()}
			</div>
		)
	},

	renderView () {
		if (this.props.isShowingClass) return <Class {...this.props.class} students={this.props.studentsByClass} showClasses={this.props.showClasses} />
		return <Classes classes={this.props.classes} showClass={this.props.showClass} />
	}
})
