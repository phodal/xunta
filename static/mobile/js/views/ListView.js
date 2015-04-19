define([
	'jquery',
	'backbone',
	'underscore',
	'mustache'
], function ($, Backbone, _, Mustache) {
	'use strict';
	var ListView = Backbone.View.extend ({
		el: $("#content"),

		initialize: function(collection, template, model){
			var that = this;
			this.beforeRender();
			this.template = template;
			this.model = model;
			this.collection = collection;

			this.collection.fetch({
				data: { limit: 30 },
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

	return ListView;
});