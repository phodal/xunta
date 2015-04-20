define([
	'jquery',
	'underscore',
	'backbone',
	'js/router',
	'jquerySidr',
], function($, _, Backbone, AppRouter){
	var initialize = function(){
		$(document).ready(function() {
			$('#sidr').show();
			$('#menu').sidr();
		});
		new AppRouter();
	};

	return {
		initialize: initialize
	};
});
