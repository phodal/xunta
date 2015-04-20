require.config({
	//baseUrl: '/static/mobile/', //build
	baseUrl: '/static/mobile/',
	paths: {
		'text': 'js/lib/text',
		jquery: 'js/lib/jquery.min',
		json: 'js/lib/json',
		appRouter: 'js/router',
		templates: 'templates',
		jquerySidr: 'js/lib/jquery.sidr.min',
		underscore: 'js/lib/lodash.min',
		mustache: 'js/lib/mustache',
		backbone: 'js/lib/backbone',
		app: 'js/app'
	},
	shim: {
		jquerySidr:["jquery"],
		underscore: {
			exports: '_'
		}
	}
});

require(['app'], function(App){
	App.initialize();
});