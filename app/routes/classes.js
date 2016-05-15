require('dotenv').load()
var config = require('../../config')
var express = require('express')
var request = require('request')
var router = express.Router()

router.use(function (req, res, next) {
	console.log('Routing Classes...', req.url)
	next()
})

router.get('/', function (req, res) {
	var data = {
		app: 'classes',
	}

	res.render('index', { data: data })
})


module.exports = router
