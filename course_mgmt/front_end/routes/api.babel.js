var express = require('express')
var request = require('request')

var classes = require('./classes.babel')
var students = require('./students.babel')

var router = express.Router()

router.use('/classes', classes)
router.use('/students', students)

module.exports = router
