define([
	'jquery',
	'underscore',
	'backbone',
	'router',
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
			$("#sidr li a" ).bind('touchstart click', function() {
				if(null != Backbone.history.fragment){
					_.each($("#sidr li"),function(li){
						$(li).removeClass()
					});

					$('a[href$="#/'+Backbone.history.fragment+'"]').parent().addClass("active");
					$.sidr('close');
					window.scrollTo(0,0);
				}
			});
		});
		AppRouter.initialize();
	};

	return {
		initialize: initialize
	};
});