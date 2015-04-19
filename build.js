({
	baseUrl: 'static/mobile/',
	paths: {
		'text': 'js/lib/text',
		jquery: 'js/lib/jquery.min',
		json: 'js/lib/json',
		appRouter: 'js/router',
		templates: 'templates',
		jquerySidr: 'js/lib/jquery.sidr.min',
		touchwipe: 'js/lib/jquery.touchwipe.min',
		underscore: 'js/lib/lodash.min',
		mustache: 'js/lib/mustache',
		backbone: 'js/lib/backbone'
	},
	shim: {
		jquerySidr:["jquery"],
		touchwipe: ["jquery"],
		underscore: {
			exports: '_'
		}
	},
    name: "js/main",
    out: "static/mobile/build/build.js",
    removeCombined: true
});