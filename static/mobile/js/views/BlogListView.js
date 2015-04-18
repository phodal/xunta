define([
	'jquery',
	'backbone',
	'underscore',
	'mustache',
	'text!/static/mobile/templates/blog_list.html',
	'js/model/BlogModel'
],function($, Backbone, _, Mustache, blogListTemplate, BlogCollection){
	'use strict';
	var BlogListView = Backbone.View.extend ({
		el: $("#content"),

		initialize: function(){
			var that = this;
			this.collection = new BlogCollection();
			this.collection.fetch({
				data: {limit: 20},
				success: function(){
					that.render();
				}
			});
		},
		render: function(){
			var items= this.collection.toJSON()[0];
			console.log(items.results);
			this.$el.html(Mustache.to_html(blogListTemplate, { blog: items.results }));
		}
	});

	return BlogListView;
});