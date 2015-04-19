define([
	'jquery',
	'backbone',
	'underscore',
	'mustache',
	'text!/static/mobile/templates/juba_list.mustache',
	'js/model/JubaModel'
],function($, Backbone, _, Mustache, jubaListTemplate, JubaCollection){
	'use strict';
	var JubaListView = Backbone.View.extend ({
		el: $("#content"),

		initialize: function(){
			var that = this;
			this.beforeRender();
			this.collection = new JubaCollection();
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
			this.$el.html(Mustache.to_html(jubaListTemplate, { juba: items.results }));
		}
	});

	return JubaListView;
});