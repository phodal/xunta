define([
	'jquery',
	'backbone',
	'underscore',
	'mustache',
	'text!/static/mobile/templates/juba_detail.html',
	'js/model/JubaModel'
],function($, Backbone, _, Mustache, jubaDetailTemplate, JubaCollection){
	'use strict';
	var JubaView = Backbone.View.extend ({
		el: $("#content"),

		initialize: function(jubaSlug){
			var that = this;
			this.collection = new JubaCollection();
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
			console.log(items.results)
			this.$el.html(Mustache.to_html(jubaDetailTemplate, { juba: items.results }));
		},
		afterRender: function() {
			$("img").addClass("pure-img");
		}
	});

	return JubaView;
});