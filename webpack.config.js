var webpack = require('webpack');
var config = require('config.js')

module.exports = {
	entry: config.paths.PUBLIC + 'js/app.js',
	output: {
		path: config.paths.PUBLIC + '/js/build',
		filename: 'bundle.js',
	},
	module: {
		loaders: [
			{
				test: /\.js?$/,
				exclude: /(node_modules|bower_components)/,
				loader: 'babel',
			},
			{
				test: /\.jsx?$/,
				exclude: /(node_modules|bower_components)/,
				loader: 'babel',
			}
		]
	},
	resolve: {
		extensions: ['', '.js', '.jsx', '.json']
	}
}
