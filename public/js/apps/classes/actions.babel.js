var $ = require('jquery')
var actions = require('./constants').ACTIONS

module.exports = {
	setup (options) {
		return dispatch => {
			dispatch(this.toggleLoading(true))

			$.when(
				dispatch(this.fetchClasses())
			).done(() => {
				dispatch(this.toggleLoading(false))
			})
		}
	},

	fetchClasses () {
		return dispatch =>
			$.get('/api/classes')
				.done((res) => {
					dispatch(this.receiveClasses(res))
				})
	},

	receiveClasses (classes) {
		return {
			type: actions.RECEIVE_CLASSES,
			payload: {
				classes,
			}
		}
	},

	toggleLoading (value) {
		return {
			type: actions.TOGGLE_LOADING,
			payload: {
				value,
			}
		}
	}
}
