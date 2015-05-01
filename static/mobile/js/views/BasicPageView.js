define([
	'jquery',
	'backbone',
	'underscore',
	'mustache'
], function ($, Backbone, _, Mustache) {
	'use strict';
	var BasicPageView = Backbone.View.extend ({
		el: $("#content"),

		initialize: function(collection, template, model, options){
			var that = this, data;
			this.beforeRender();
			this.template = template;
			this.model = model;
			this.collection = collection;


			if(options) {
				data =  {search: options.slug}
			} else {
				data = { limit: 30 };
			}

			this.collection.fetch({
				data: data,
				success: function(){
					that.render(that.template, that.model);
					that.afterRender();
				}
			});
		},
		beforeRender: function () {
			$.sidr('close');
		},
		render: function(template, model){
			var obj = "objname";
			var items= this.collection.toJSON()[0];

			this.objname = {};
			this[obj][model] = items.results;

			this.$el.html(Mustache.to_html(template, this.objname ));
		},
		afterRender: function() {
			$("img").addClass("pure-img");
		}
	});

	return BasicPageView;
});