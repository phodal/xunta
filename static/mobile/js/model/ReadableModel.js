"use strict";

define(['backbone'], function(Backbone) {
    var ReadableModel = Backbone.Model.extend({});

    var Readable = Backbone.Collection.extend({
        model: ReadableModel,
        url: '/api/all',
        parse: function (data) {
            return data;
        }
    });
    return Readable;
});