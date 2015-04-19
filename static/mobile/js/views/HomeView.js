define([
	'jquery',
	'backbone',
	'underscore',
	'mustache',
	'text!/static/mobile/templates/homepage_detail.mustache',
	'js/model/ReadableModel'
],function($, Backbone, _, Mustache, homepageTemplate, ReadableModel){
	'use strict';
	var HomeView = Backbone.View.extend ({
		el: $("#content"),

		initialize: function(){
			var that = this;
			this.beforeRender();
			this.collection = new ReadableModel();
			this.collection.fetch({
				success: function(){
					that.render();
				}
			});
		},
		beforeRender: function () {
			$.sidr('close');
		},
		render: function(){
			var items= this.collection.toJSON();
			var blog = _.where(items, { 'model': 'blog' });
			var juba = _.where(items, { 'model': 'juba' });
			var link = _.where(items, { 'model': 'link' });

			this.$el.html(Mustache.to_html(homepageTemplate, { blog: blog, juba:juba, link:link}));
		}
	});

	return HomeView;
});