"use strict";

define(['backbone'], function(Backbone) {
    var BlogModel = Backbone.Model.extend({});

    var BlogList = Backbone.Collection.extend({
        model: BlogModel,
        url: '/api/blog_list/',
        parse: function (data) {
            return data;
        }
    });
    return BlogList;
});