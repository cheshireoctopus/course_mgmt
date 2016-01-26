module.exports = {
	paths: {
		PUBLIC: './public/',
		GITHUB: './app/routes/'
	},
	githubAPI: {
		authUser: 'https://github.com/login/oauth/authorize',
		getUser: 'https://api.github.com/users/',
		queryUser: 'https://api.github.com/search/users',
	},
}
