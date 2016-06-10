var Model = require('data/model.babel')
var constants = require('constants')

module.exports = Model.extend({
	url () {
		return constants.API.COURSE + this.id
	},
})
