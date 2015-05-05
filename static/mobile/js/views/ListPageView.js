define([
	'jquery',
	'backbone',
	'underscore',
	'mustache'
], function ($, Backbone, _, Mustache) {
	'use strict';
	var ListPageView = Backbone.View.extend ({
		el: "#content",

		initialize: function (collection, template, model) {
			var that = this;
			this.beforeRender();
			this.template = template;
			this.model = model;
			this.collection = collection;
			this.page = 0;
			this.results = {};

			$( document ).on( "scroll", function(){
				if( $(window).scrollTop() + $( window ).height() >= $( "#content" ).height() ) {
					if(that.hasNext) {
						that.loadResults();
					}
				}
			});

			that.loadResults();
		},
		beforeRender: function () {
			$.sidr('close');
		},
		render: function(template, model){
			var obj = "objname", that = this, items= this.collection.toJSON()[0];

			this.objname = {};
			this[obj][model] = items.results;
			if(that.page === 0) {
				this.$el.html(Mustache.to_html(template, this.objname ));
			} else {
				if(items.next !== null) {
					that.hasNext = true;
					$(that.el).append(Mustache.to_html(template, this.objname ));
				} else {
					that.hasNext = false;
					$(that.el).append(Mustache.to_html(template, this.objname ));
				}
			}
		},
		loadResults: function(){
			var that = this;
			var offset = this.page * 30;

			this.collection.fetch({
				data: { limit: 30, offset: offset},
				success: function(){
					that.page += 1;
					that.render(that.template, that.model);
				}
			});
		}
	});

	return ListPageView;
});