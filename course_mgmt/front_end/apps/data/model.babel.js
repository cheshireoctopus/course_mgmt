var Backbone = require('backbone')

module.exports = Backbone.Model.extend({
	parse (res) {
		return res.data || res
	}
})
