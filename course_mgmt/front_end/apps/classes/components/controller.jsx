var React = require('react')
var Class = require('classes/components/class.jsx')
var Classes = require('classes/components/classes.jsx')
var ClassForm = require('classes/components/class_form.jsx')

module.exports = React.createClass({
	displayName: 'ClassesController',

	propTypes: {
		classObj: React.PropTypes.object.isRequired,
		classes: React.PropTypes.array.isRequired,
		courses: React.PropTypes.array.isRequired,
		deleteClass: React.PropTypes.func.isRequired,
		onEditClass: React.PropTypes.func.isRequired,
		isLoading: React.PropTypes.bool.isRequired,
		isShowingClass: React.PropTypes.bool.isRequired,
		isShowingForm: React.PropTypes.bool.isRequired,
		showClass: React.PropTypes.func.isRequired,
		showClasses: React.PropTypes.func.isRequired,
		studentsByClass: React.PropTypes.array.isRequired,
		saveClass: React.PropTypes.func.isRequired,
		onShowForm: React.PropTypes.func.isRequired,
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
				{this.props.isShowingForm ? this.renderForm() : this.renderClasses()}
			</div>
		)
	},

	renderClasses () {
		if (this.props.isLoading) return <h3>Loading...</h3>
		if (this.props.isShowingClass)
			return <Class {...this.props.classObj}
					onEdit={this.props.onEditClass}
					onDelete={this.props.deleteClass}
					students={this.props.studentsByClass}
					showClasses={this.props.showClasses}
					/>


		return <Classes
					classes={this.props.classes}
					showClass={this.props.showClass}
					onShowForm={this.props.onShowForm}
				/>
	},

	renderForm () {
		return <ClassForm
				classObj={this.props.classObj}
				courses={this.props.courses}
				onClose={this.props.showClasses}
				onSave={this.props.saveClass}
				/>
	}
})
