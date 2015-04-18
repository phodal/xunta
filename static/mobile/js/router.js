"use strict";

define([
    'jquery',
    'underscore',
    'backbone',
    'static/mobile/js/views/HomeView.js',
    'static/mobile/js/views/BlogView.js',
    'static/mobile/js/views/BlogListView.js',
],function($, _, Backbone, HomeView, BlogView, BlogListView){
    var AppRouter = Backbone.Router.extend({
        index: function(){
            var homeView = new HomeView();
            homeView.render();
        },
        blog: function(blogSlug){
            var loginView = new BlogView(blogSlug);
            loginView.render();
        },
        blogList: function(blogSlug){
            var loginView = new BlogListView();
            loginView.render();
        },
        initialize: function() {
            var router = this,
                routes = [
                    [ /^.*$/, "index" ],
                    [ 'blog', "blogList" ],
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
