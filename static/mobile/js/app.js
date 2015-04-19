define([
	'jquery',
	'underscore',
	'backbone',
	'js/router',
	'jquerySidr',
	'touchwipe'
], function($, _, Backbone, AppRouter){
	var initialize = function(){
		$(window).touchwipe({
			wipeLeft: function() {
				$.sidr('close');
			},
			wipeRight: function() {
				$.sidr('open');
			},
			preventDefaultEvents: false
		});
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
