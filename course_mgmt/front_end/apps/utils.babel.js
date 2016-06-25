module.exports = {
	githubUserProfile: githubUserProfile,
}

function githubUserProfile (username) {
if (!username) return false
	return 'https://github.com/' + username
}
