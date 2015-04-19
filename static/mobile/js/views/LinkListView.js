define([
	'jquery',
	'backbone',
	'underscore',
	'mustache',
	'text!/static/mobile/templates/link_list.mustache',
	'js/model/LinkModel'
],function($, Backbone, _, Mustache, linkListTemplate, LinkCollection){
	'use strict';
	var LinkListView = Backbone.View.extend ({
		el: $("#content"),

		initialize: function(){
			var that = this;
			this.beforeRender();
			this.collection = new LinkCollection();
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
		beforeRender: function () {
			$.sidr('close');
		},
		render: function(){
			var items= this.collection.toJSON()[0];
			this.$el.html(Mustache.to_html(linkListTemplate, { link: items.results }));
		}
	});

	return LinkListView;
});