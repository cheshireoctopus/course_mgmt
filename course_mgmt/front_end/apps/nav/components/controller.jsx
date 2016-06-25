var _ = require('underscore')
var React = require('react')
var NavLink = require('nav/components/nav_link.jsx')
var constants = require('nav/constants.js')

const MAIN = 'classes'

module.exports = React.createClass({
	displayName: 'NavController',

	propTypes: {
		app: React.PropTypes.string.isRequired,
		onNavClick: React.PropTypes.func.isRequired,
	},

	render () {
		let links = _.map(constants.LINKS, (link, i) => {
			return <NavLink key={i} {...link} onNavClick={this.props.onNavClick} isActive={link === this.props.app} />
		})

		return (
			<nav className="navbar navbar-default">
				<div className="container-fluid">
					<div className="navbar-header">
						<button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
							<span className="sr-only">Toggle navigation</span>
							<span className="icon-bar"></span>
							<span className="icon-bar"></span>
							<span className="icon-bar"></span>
						</button>
						<a className="navbar-brand" href="javascript:void(0)" onClick={this.renderMain}>Course MGMT</a>
					</div>
					<div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
						<ul className="nav navbar-nav">
							{links}
						</ul>
					</div>
				</div>
			</nav>
		)
	},

	renderMain () {
		this.props.onNavClick(MAIN)
	}
})
