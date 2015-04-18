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
		page: 0,
		el: $("#content"),

		initialize: function(){
			var that = this;
			this.collection = new BlogCollection();
			this.collection.fetch({
				data: { limit: 30 },
				success: function(){
					$(".loading").hide();
					that.render();
				}
			});
			$(window).scroll(function() {
				if($(window).scrollTop() + $(window).height() == $(document).height()) {

				}
			});
		},
		render: function(){
			var items= this.collection.toJSON()[0];
			this.$el.html(Mustache.to_html(blogListTemplate, { blog: items.results }));
		}
	});

	return BlogListView;
});