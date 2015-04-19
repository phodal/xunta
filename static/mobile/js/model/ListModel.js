"use strict";

define(['backbone'], function(Backbone) {
    var LinkModel = Backbone.Model.extend({});

    var Link = Backbone.Collection.extend({
        initialize: function(url) {
            this.url = url;
        },
        model: LinkModel,
        url: function () {
            return this.url;
        },
        parse: function (data) {
            return data;
        }
    });
    return Link;
});