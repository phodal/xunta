"use strict";

define([
    'jquery',
    'underscore',
    'backbone',
    'static/mobile/js/views/HomeView.js'
],function($, _, Backbone, HomeView){
    var AppRouter = Backbone.Router.extend({
        index: function(){
            var homeView = new HomeView();
            homeView.initialize();
        },
        initialize: function() {
            var router = this,
                routes = [
                    [ /^.*$/, "index" ]
                ];

            _.each(routes, function(route) {
                router.route.apply(router,route);
            });

            Backbone.history.start();
        }
    });

    return AppRouter;
});
