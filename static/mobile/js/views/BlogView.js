define([
	'jquery',
	'backbone',
	'underscore',
	'mustache',
	'text!/static/mobile/templates/blog_detail.html',
	'js/model/BlogModel'
],function($, Backbone, _, Mustache, blogDetailTemplate, BlogCollection){
	'use strict';
	var BlogView = Backbone.View.extend ({
		el: $("#content"),

		initialize: function(blogSlug){
			var that = this;
			this.collection = new BlogCollection();
			this.collection.fetch({
				data: {search: blogSlug},
				success: function(){
					that.render();
					that.afterRender();
				}
			});
		},

		render: function(){
			var items= this.collection.toJSON()[0];
			this.$el.html(Mustache.to_html(blogDetailTemplate, { blog: items.results }));
		},
		afterRender: function() {
			$("img").addClass("pure-img");
		}
	});

	return BlogView;
});