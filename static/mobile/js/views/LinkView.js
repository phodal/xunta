define([
	'jquery',
	'backbone',
	'underscore',
	'mustache',
	'text!/static/mobile/templates/link_detail.mustache',
	'js/model/JubaModel'
],function($, Backbone, _, Mustache, linkDetailTemplate, LinkCollection){
	'use strict';
	var LinkView = Backbone.View.extend ({
		el: $("#content"),

		initialize: function(jubaSlug){
			var that = this;
			this.collection = new LinkCollection();
			this.collection.fetch({
				data: {search: jubaSlug},
				success: function(){
					that.render();
					that.afterRender();
				}
			});
		},

		render: function(){
			var items= this.collection.toJSON()[0];
			this.$el.html(Mustache.to_html(linkDetailTemplate, { link: items.results }));
		},
		afterRender: function() {
			$("img").addClass("pure-img");
		}
	});

	return LinkView;
});