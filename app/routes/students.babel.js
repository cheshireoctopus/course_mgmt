var express = require('express')
var router = express.Router()

var studentsData = require('../../tests/fixtures/students.json')
var studentData = require('../../tests/fixtures/student.json')

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
	var classId = req.params.id

	console.log('CLASS ID: ' + classId)

	res.send(studentsData)
})

module.exports = router
