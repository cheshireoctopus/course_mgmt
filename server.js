require('dotenv').load()
var config = require('./config')

var express = require('express')
var path = require('path')

var githubRouter = require(config.paths.GITHUB + '/github.js')
var classesRouter = require(config.paths.ROUTES + '/classes.js')

var app = express()

// Set template engine
app.set('view engine', 'jade')
app.set('views', config.paths.VIEWS)

// Middleware
app.use(express.static(config.paths.PUBLIC))

app.use(function (req, res, next) {
	console.log('Routing...', req.url)
	next()
})

// Catch-all error handler
app.use(function (err, req, res, next) {
	console.log(err.stack)
	res.status(500)
	res.render('error', { error: err });
})

// Routes
app.use('/classes', classesRouter)
app.use('/github', githubRouter)

app.get('/', function (req, res) {
	var data = {
		app: 'index',
	}

	res.render('index', { data: data })
})

// Get turnt
app.listen(process.env.PORT, function () {
	console.log('shit is going down on ' + process.env.PORT)
})
