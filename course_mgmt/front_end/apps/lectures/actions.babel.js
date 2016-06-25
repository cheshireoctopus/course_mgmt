var $ = require('jquery')
var _ = require('underscore')
var Immutable = require('immutable')
var actions = require('lectures/constants').ACTIONS
var API = require('constants.js').API

module.exports = {
	setup () {
		return dispatch => {
			dispatch(toggleLoading(true))

			$.when(
				dispatch(fetchLectures()),
				dispatch(fetchCourses())
			)
			.then(() => dispatch(toggleLoading(false)))
		}
	},

	onShowForm () {
		return dispatch => dispatch(renderForm())
	},

	onSaveForm (lecture) {
		return dispatch => {
			dispatch(toggleLoading(true))

			if (lecture.id) return dispatch(editLecture(lecture))
			return dispatch(createLecture(lecture))
		}
	},

	onDeleteLecture (lectureId) {
		let data = {
			data: [{ id: lectureId }]
		}

		return dispatch => {
			dispatch(toggleLoading(true))

			$.ajax({
				url: API.LECTURE,
				type: 'DELETE',
				data: JSON.stringify(data),
				contentType: 'application/JSON',
			})
			.then(() => {
				$.when(
					dispatch(fetchLectures())
				)
				.then(() => {
					dispatch(renderLectures())
					dispatch(toggleLoading(false))
				})
			})
		}
	},

	onShowLecture (lectureId) {
		return (dispatch, getState) => {
			dispatch(toggleLoading(true))

			$.get(API.LECTURE + lectureId + '/?data=course,class')
				.then(res => {
					dispatch(receiveLecture(res.data))
					dispatch(renderLecture())
					dispatch(toggleLoading(false))
				})
		}
	},

	onShowLectures () {
		return {
			type: actions.RENDER_LECTURES
		}
	},
}

function toggleLoading (value) {
	return {
		type: actions.TOGGLE_LOADING,
		payload: {
			value,
		}
	}
}

// PERSIST
function editLecture (lecture) {

}

function createLecture (lecture) {
	let data = {
		data: [lecture]
	}

	return (dispatch, getState) => {
		$.ajax({
			url: API.LECTURE,
			type: 'POST',
			data: JSON.stringify(data),
			contentType: 'application/JSON',
		})
		.then(res => {
			$.when(
				dispatch(fetchLectures())
			)
			.then(() => {
				dispatch(renderLectures())
				dispatch(toggleLoading(false))
			})
		})
	}
}

// FETCH
function fetchCourses () {
	return dispatch => {
		$.get(API.COURSE)
			.then(res => dispatch(receiveCourses(res.data)))
	}
}

function fetchLectures () {
	return dispatch => {
		$.get(API.LECTURE)
			.then(res => dispatch(receiveLectures(res.data)))
	}
}

// RECEIVE
function receiveCourses (courses) {
	return {
		type: actions.RECEIVE_COURSES,
		payload: {
			courses,
		}
	}
}

function receiveLecture (lecture) {
	return {
		type: actions.RECEIVE_LECTURE,
		payload: {
			lecture,
		}
	}
}

function receiveLectures (lectures) {
	return {
		type: actions.RECEIVE_LECTURES,
		payload: {
			lectures,
		}
	}
}

// RENDER
function renderForm () {
	return {
		type: actions.RENDER_FORM,
	}
}

function renderLecture () {
	return {
		type: actions.RENDER_LECTURE,
	}
}

function renderLectures () {
	return {
		type: actions.RENDER_LECTURES,
	}
}
