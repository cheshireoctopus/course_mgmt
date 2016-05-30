require('dotenv').load()
var config = require('../../config')
var express = require('express')
var request = require('request')
var router = express.Router()

router.use(function (req, res, next) {
	console.log('Routing GitHub...', req.url)
	next()
})

// Query user by username
router.route('/search/users/:query')
	.get(function (req, res) {
		var query = req.params.query
		var options = {
			url: config.githubAPI.queryUser,
			qs: {
				q: query,
				client_id: process.env.githubClientId,
				client_secret: process.env.githubClientSecret
			},
			headers: {
				'User-Agent': process.env.githubUsername
			}
		}

		var r = request(options, function (error, response, body) {
	  		if (!error && response.statusCode == 200) {
	    		res.setHeader('Content-Type', 'application/json')
	    		res.send(body)
			} else {
				res.setHeader('Content-Type', 'application/json')
				res.send(body)
			}
		})
	})

// Get user by username
router.route('/user/:username')
	.get(function (req, res) {
		var username = req.params.username
		var options = {
			url: config.githubAPI.getUser + username,
			headers: {
				'User-Agent': process.env.githubUsername
			}
		}

		var r = request(options, function (error, response, body) {
	  		if (!error && response.statusCode == 200) {
	    		res.setHeader('Content-Type', 'application/json')
	    		res.send(body)
			} else {
				res.setHeader('Content-Type', 'application/json')
				res.send(body)
			}
		})
	})

// Get user's repos
router.route('/repos/:username')
	.get(function (req, res) {
		var username = req.params.username
		var options = {
			url: config.githubAPI.getUser + username + '/repos' ,
			headers: {
				'User-Agent': process.env.githubUsername
			}
		}

		var r = request(options, function (error, response, body) {
			if (!error && response.statusCode == 200) {
				res.setHeader('Content-Type', 'application/json')
				res.send(body)
			}
		})
	})

module.exports = router
