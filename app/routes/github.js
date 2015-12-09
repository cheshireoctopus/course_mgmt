require('dotenv').load()
var config = require('../../config')

var express = require('express')
var request = require('request')

// Router instance
var router = express.Router()

// Middleware
router.use(function (req, res, next) {
	console.log('Routing GitHub...', req.url)
	next()
})

router.route('/user/:username')
	.get(function (req, res) {
		var username = req.params.username
		var options = {
			url: config.githubAPI.getUser + username,
			headers: {
				'User-Agent': process.env.githubUsername
			}
		}

		var req = request(options, function (error, response, body) {
	  		if (!error && response.statusCode == 200) {
	    		res.setHeader('Content-Type', 'application/json')
	    		res.send(body)
			}
		})
	})

router.route('/repos/:username')
	.get(function (req, res) {
		var username = req.params.username
		var options = {
			url: config.githubAPI.getUser + username + '/repos' ,
			headers: {
				'User-Agent': process.env.githubUsername
			}
		}

		var req = request(options, function (error, response, body) {
			if (!error && response.statusCode == 200) {
				res.setHeader('Content-Type', 'application/json')
				res.send(body)
			}
		})
	})

module.exports = router
