define([
	'jquery',
	'backbone',
	'underscore',
	'mustache',
	'text!/static/mobile/templates/homepage_detail.html',
	'js/model/ReadableModel'
],function($, Backbone, _, Mustache, homepageTemplate, ReadableModel){
	'use strict';
	var HomeView = Backbone.View.extend ({
		el: $("#content"),

		initialize: function(){
			var that = this;
			this.collection = new ReadableModel();
			this.collection.fetch({
				success: function(){
					that.render();
				}
			});
		},
		render: function(){
			var items= this.collection.toJSON();
			this.$el.html(Mustache.to_html(homepageTemplate, { items: items}));
		}
	});

	return HomeView;
});