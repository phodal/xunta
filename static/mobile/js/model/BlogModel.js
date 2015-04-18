"use strict";

define(['backbone'], function(Backbone) {
    var BlogModel = Backbone.Model.extend({});

    var Blog = Backbone.Collection.extend({
        model: BlogModel,
        url: '/api/blog_detail/',
        parse: function (data) {
            return data;
        }
    });
    return Blog;
});