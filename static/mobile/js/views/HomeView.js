define([
	'jquery',
	'backbone',
	'underscore',
	'mustache',
	'text!/static/mobile/templates/homepage_detail.html'
],function($, Backbone, _, Mustache, homepageTemplate){
	'use strict';
	var HomeView = Backbone.View.extend ({
		el: $("#content"),

		initialize: function(){

		},
		render: function(){
			this.$el.html(Mustache.to_html(homepageTemplate, {data: "hello"}));
		}
	});

	return HomeView;
});