var express = require('express')

var router = express.Router()

router.use(function (req, res, next) {
	console.log('Routing Students...', req.url)
	next()
})

router.get('/', function (req, res) {
	res.send('STUDENTS')
})

router.get('/:id', function (req, res) {
	res.send('STUDENT')
})

router.get('/class/:id', function (req, res) {
	res.send('STUDENTS BY CLASS')
})

module.exports = router
