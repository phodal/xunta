"use strict";

define(['backbone'], function(Backbone) {
	var LinkModel = Backbone.Model.extend({});

	var Link = Backbone.Collection.extend({
		model: LinkModel,
		url: '/api/link_detail/',
		parse: function (data) {
			return data;
		}
	});
	return Link;
});