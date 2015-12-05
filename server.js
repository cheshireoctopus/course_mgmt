require('dotenv').load()

var config = require('./config')

var express = require('express')
var path = require('path')

var request = require('request')

var app = express()

// Middleware
app.use(express.static(config.paths.PUBLIC))

// Routes
app.get('/', function (req, res) {
	res.sendFile(path.join(config.paths.PUBLIC))
})

// GET github username
app.get('/user', function (req, res) {
	var username = req.query['username']

	var options = {
		url: config.githubAPI.getUser + username,
		headers: {
			'User-Agent': 'cheshireoctopus'
		}
	}

	var resp = request(options, function (error, response, body) {
  		if (!error && response.statusCode == 200) {
    		console.log(body)
    		res.send(body)
		}
	})

})

// Get turnt
app.listen(process.env.PORT, function () {
	console.log('shit is going down on ' + process.env.PORT)
})
