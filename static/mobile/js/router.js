"use strict";

define([
    'jquery',
    'underscore',
    'backbone',
    'static/mobile/js/views/HomeView.js',
    'static/mobile/js/views/BlogView.js',
],function($, _, Backbone, HomeView, BlogView){
    var AppRouter = Backbone.Router.extend({
        index: function(){
            var homeView = new HomeView();
            homeView.render();
        },
        blog: function(blogSlug){
            var loginView = new BlogView(blogSlug);
            loginView.render();
        },
        initialize: function() {
            var router = this,
                routes = [
                    [ /^.*$/, "index" ],
                    [ 'blog/*slug', "blog" ]
                ];

            _.each(routes, function(route) {
                router.route.apply(router,route);
            });

            Backbone.history.start();
        }
    });

    return AppRouter;
});
