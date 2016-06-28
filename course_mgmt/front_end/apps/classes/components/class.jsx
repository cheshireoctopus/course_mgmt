var _ = require('underscore')
var React = require('react')
var DateTime = require('components/date_time.jsx')
var UserImage = require('components/user_image.jsx')
var utils = require('utils.babel')

module.exports = React.createClass({
	displayName: 'Class',

	propTypes: {
		description: React.PropTypes.string,
		end_dt: React.PropTypes.string,
		homeworks: React.PropTypes.array.isRequired,
		id: React.PropTypes.number.isRequired,
		lectures: React.PropTypes.array.isRequired,
		location: React.PropTypes.string,
		name: React.PropTypes.string,
		start_dt: React.PropTypes.string,
		students: React.PropTypes.array.isRequired,
		showClasses: React.PropTypes.func.isRequired,
		onEdit: React.PropTypes.func.isRequired,
		onDelete: React.PropTypes.func.isRequired
	},

	getInitialState () {
		return {
			activeTab: 'students'
		}
	},

	render () {
		let activeTab = this.state.activeTab

		return (
			<div className="row">
				<div className="col-md-12">
					<a onClick={this.props.showClasses}>Back to Main</a>
				</div>
				<div className="col-md-12">
					<h2>{this.props.name}</h2>
					<p>Start: <DateTime date={this.props.start_dt} /></p>
					<p>End: <DateTime date={this.props.end_dt} /></p>
					<p>Location: {this.props.location || 'N/A'}</p>
					<p>Student Count: {this.props.students.length}</p>
					<button className="btn btn-warning push-right" onClick={this.handleEdit}>Edit</button>
					<button className="btn btn-danger" onClick={this.handleDelete}>Delete</button>
					<hr/>
				</div>
				<div className="col-md-12">
					<ul className="nav nav-tabs">
						<li  onClick={this.setActiveTab.bind(this, 'students')} className={activeTab === 'students' ? 'active' : null}><a href="javascript:void(0)">Students</a></li>
						<li onClick={this.setActiveTab.bind(this, 'lectures')} className={activeTab === 'lectures' ? 'active' : null} ><a href="javascript:void(0)">Lectures</a></li>
						<li onClick={this.setActiveTab.bind(this, 'homework')} className={activeTab === 'homework' ? 'active' : null}><a href="javascript:void(0)">Homework</a></li>
					</ul>
					<div className="tab-content">
					    <div className="tab-pane active">
							{activeTab === 'students' ? this.renderStudents() : null}
							{activeTab === 'lectures' ? this.renderLectures() : null}
							{activeTab === 'homework' ? this.renderHomework() : null}
					    </div>
					</div>
				</div>
			</div>
		)
	},

	setActiveTab (tab) {
		this.setState({
			activeTab: tab,
		})
	},

	renderStudents () {
		if (!this.props.students.length) return <h4>You haven't added any students to this class yet.</h4>

		let students = _.map(this.props.students, student => {
			return (
				<tr key={student.id}>
					<td className="text-center">
						<UserImage size={40} imgSrc={student.photo_url} />
					</td>
					<td>{student.first_name}</td>
					<td>{student.last_name}</td>
					<td><a onClick={e => {e.stopPropagation()}} href={utils.githubUserProfile(student.github_username)}>{student.github_username}</a></td>
					<td>{student.email}</td>
				</tr>
			)
		})

		return (
			<table className="table table-bordered table-condensed table-striped">
				<thead>
					<tr>
						<th></th>
						<th>First Name</th>
						<th>Last Name</th>
						<th>GitHub</th>
						<th>Email</th>
					</tr>
				</thead>
				<tbody>{students}</tbody>
			</table>
		)
	},

	renderLectures () {
		if (!this.props.lectures.length) return <h4>You haven't added any lectures to this class yet.</h4>

		let lectures = _.map(this.props.lectures, lecture => {
			return (
				<tr key={lecture.id}>
					<td>{lecture.name}</td>
					<td>{lecture.description}</td>
				</tr>
			)
		})

		return (
			<table className="table table-bordered table-condensed table-striped">
				<thead>
					<tr>
						<th>Lecture Name</th>
						<th>Description</th>
					</tr>
				</thead>
				<tbody>{lectures}</tbody>
			</table>
		)
	},

	renderHomework () {
		if (!this.props.homeworks.length) return <h4>You haven't added any homework to this class yet.</h4>

		return (
			<table className="table table-bordered table-condensed table-striped">
				<thead>
					<tr>
						<th>Homework Name</th>
						<th>Description</th>
					</tr>
				</thead>
				<tbody></tbody>
			</table>
		)
	},

	handleEdit () {
		this.props.onEdit(this.props.id)
	},

	handleDelete () {
		this.props.onDelete(this.props.id)
	},
})
