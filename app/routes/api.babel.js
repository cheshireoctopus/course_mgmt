var express = require('express')
var request = require('request')

var classes = require('./classes.babel')

var router = express.Router()

router.use('/classes', classes)

module.exports = router
