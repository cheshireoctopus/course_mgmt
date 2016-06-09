var Backbone = require('backbone')

module.exports = Backbone.Collection.extend({
	parse (res) {
		return res.data || res
	}
})
