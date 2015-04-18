"use strict";

define(['backbone'], function(Backbone) {
    var JubaModel = Backbone.Model.extend({});

    var Juba = Backbone.Collection.extend({
        model: JubaModel,
        url: '/api/juba_detail/',
        parse: function (data) {
            return data;
        }
    });
    return Juba;
});