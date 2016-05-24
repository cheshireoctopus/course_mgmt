var express = require('express')
var request = require('request')

var classesData = require('../../public/js/apps/classes/__tests__/fixtures/classes.json')
var classData = require('../../public/js/apps/classes/__tests__/fixtures/class.json')

var router = express.Router()

router.use(function (req, res, next) {
	console.log('Routing Classes...', req.url)
	next()
})

router.get('/', function (req, res) {
	res.send(classesData)
})

module.exports = router
