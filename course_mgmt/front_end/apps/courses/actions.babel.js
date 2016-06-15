var $ = require('jquery')
var actions = require('courses/constants.js').ACTIONS
var API = require('constants.js').API
var _ = require('underscore')
var Course = require('data/models/course.babel')
var Courses = require('data/collections/courses.babel')

module.exports = {
	setup (options) {
		return dispatch => {
			dispatch(toggleLoading(true))

			$.when(
				dispatch(fetchCourses(options.courses))
			).then(() => {
				dispatch(toggleLoading(false))
			})
		}
	},

	deleteCourse (courseId) {
		return (dispatch, getState) => {
			dispatch(toggleLoading(true))

			let data = {
				data: [{ id: courseId }]
			}

			$.ajax({
				url: API.COURSE,
				type: 'DELETE',
				contentType: 'application/json',
				data: JSON.stringify(data),
			})
			.done(() => {
				let courses = getState().get('courses').filter(course => course.id !== courseId)
				let collection = new Courses(courses.toJS())

				dispatch(receiveCourses(collection))
				dispatch(toggleLoading(false))
			})
		}
	},

	saveForm (courseName) {
		let data = {
			data: [{ name: courseName }]
		}

		return dispatch => {
			$.ajax({
				url: API.COURSE,
				type: 'POST',
				contentType: 'application/json',
				data: JSON.stringify(data),
			}).done(res => {
				dispatch(toggleForm(false))

				var course = new Course(res.data[0])

				dispatch(addCourse(course))
			})
		}
	},

	editCourse (courseId, courseName) {
		let data = {
		    data: [{
            	id: courseId,
            	name: courseName
        	}]
		}

		return (dispatch, getState) => {
			dispatch(toggleLoading(true))

			$.ajax({
				url: API.COURSE,
				type: 'PUT',
				contentType: 'application/json',
				data: JSON.stringify(data),
			})
			.then(() => {
				let courses = new Courses(getState().get('courses').toJS())
				courses.get(courseId).set({ name: courseName })

				dispatch(receiveCourses(courses))
				dispatch(toggleLoading(false))
				dispatch(toggleForm(false))
			})
		}
	},

	showCourse (courseId) {
		return dispatch => {
			dispatch(toggleLoading(true))

			$.when(
				dispatch(fetchCourseInfo(courseId))
			).then(() => {
				dispatch(toggleLoading(false))
			})
		}
	},

	showCourses () {
		return {
			type: actions.SHOW_COURSES,
		}
	},

	toggleForm (courseId) {
		return (dispatch, getState) => {
			let isShowingForm = getState().get('isShowingForm')
			let course = _.findWhere(getState().get('courses').toJS(), { id: courseId })

			dispatch(toggleForm(!isShowingForm, course))
		}
	}
}

function addCourse (course) {
	return {
		type: actions.ADD_COURSE,
		payload: { course },
	}
}

function toggleLoading (value) {
	return {
		type: actions.TOGGLE_LOADING,
		payload: { value },
	}
}

function fetchCourseInfo (id) {
	return dispatch => {
		let course = new Course({ id })
		course
			.fetch({
				data: 'data=homework,lecture,class',
			})
			.then(() => dispatch(receiveCourse(course)))
	}
}

function fetchCourses (courses) {
	return dispatch => {
		courses
			.fetch()
			.then(() => dispatch(receiveCourses(courses)))
	}
}

function receiveCourse (course) {
	return {
		type: actions.RECEIVE_COURSE,
		payload: { course },
	}
}

function receiveCourses (courses) {
	return {
		type: actions.RECEIVE_COURSES,
		payload: courses.models,
	}
}

function toggleForm (value, course) {
	return {
		type: actions.TOGGLE_FORM,
		payload: { value, course },
	}
}
