var Collection = require('data/collection.babel')
var Course = require('data/models/course.babel')
var constants = require('constants')

module.exports = Collection.extend({
	url: constants.API.COURSE,
	model: Course,
})
