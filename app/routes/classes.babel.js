var express = require('express')

var classesData = require('../../tests/fixtures/classes.json')
var classData = require('../../tests/fixtures/class.json')

var router = express.Router()

router.use(function (req, res, next) {
	console.log('Routing Classes...', req.url)
	next()
})

router.get('/', function (req, res) {
	res.send(classesData)
})

router.get('/:id', function (req, res) {
	var id = req.params.id

	res.send(classData)
})

module.exports = router
