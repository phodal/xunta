define([
	'jquery',
	'backbone',
	'underscore',
	'mustache'
], function ($, Backbone, _, Mustache) {
	'use strict';
	var ListView = Backbone.View.extend ({
		el: $("#content"),

		initialize: function(Collection, template){
			var that = this;
			this.beforeRender();
			this.template = template;

			this.collection = new Collection();
			this.collection.fetch({
				data: { limit: 30 },
				success: function(){
					that.render(that.template);
					that.afterRender();
				}
			});
		},
		beforeRender: function () {
			$.sidr('close');
		},
		render: function(template){
			var items= this.collection.toJSON()[0];
			this.$el.html(Mustache.to_html(template, { link: items.results }));
		},
		afterRender: function() {
			$("img").addClass("pure-img");
		}
	});

	return ListView;
});