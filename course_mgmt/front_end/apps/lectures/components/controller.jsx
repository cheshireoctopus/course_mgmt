var React = require('react')
var Lecture = require('lectures/components/lecture.jsx')
var Lectures = require('lectures/components/lectures.jsx')
var Form = require('lectures/components/lecture_form.jsx')

module.exports = React.createClass({
	displayName: 'LecturesController',

	propTypes: {
		courses: React.PropTypes.array.isRequired,
		lecture: React.PropTypes.object.isRequired,
		lectures: React.PropTypes.array.isRequired,
		isLoading: React.PropTypes.bool.isRequired,
		isShowingForm: React.PropTypes.bool.isRequired,
		isShowingLecture: React.PropTypes.bool.isRequired,
		onSaveForm: React.PropTypes.func.isRequired,
		onShowForm: React.PropTypes.func.isRequired,
		onDeleteLecture: React.PropTypes.func.isRequired,
		onShowLecture: React.PropTypes.func.isRequired,
		onShowLectures: React.PropTypes.func.isRequired,
	},

	render () {
		return (
			<div className="container">
				<div className="row">
					<div className="col-md-12">
						<h1>Lectures</h1>
						<hr />
					</div>
				</div>
				{this.props.isLoading ? this.renderLoading() : this.renderContent()}
			</div>
		)
	},

	renderLoading () {
		return (
			<div className="row">
				<div className="col-md-12">
					<h3>Loading...</h3>
				</div>
			</div>
		)
	},

	renderContent() {
		return this.props.isShowingForm ? this.renderForm() : this.renderLectures()
	},

	renderLectures () {
		if (this.props.isShowingLecture) {
			return <Lecture
						{...this.props.lecture}
						onDeleteLecture={this.props.onDeleteLecture}
						onShowLectures={this.props.onShowLectures}
					/>
		}

		return <Lectures
					lectures={this.props.lectures}
					onShowForm={this.props.onShowForm}
					onShowLecture={this.props.onShowLecture}
				/>
	},

	renderForm () {
		return <Form
					lecture={this.props.lecture}
					courses={this.props.courses}
					onSave={this.props.onSaveForm}
					onClose={this.props.onShowLectures}
				/>
	}
})
