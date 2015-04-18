"use strict";

define([
    'jquery',
    'underscore',
    'backbone',
    'static/mobile/js/views/HomeView.js',
    'static/mobile/js/views/BlogView.js',
    'static/mobile/js/views/BlogListView.js',
    'static/mobile/js/views/JubaView.js',
    'static/mobile/js/views/JubaListView.js',
],function($, _, Backbone, HomeView, BlogView, BlogListView, JubaView, JubaListView){
    var AppRouter = Backbone.Router.extend({
        index: function(){
            var homeView = new HomeView();
            homeView.render();
        },
        blog: function(blogSlug){
            var loginView = new BlogView(blogSlug);
            loginView.render();
        },
        blogList: function(){
            var loginView = new BlogListView();
            loginView.render();
        },
        link: function(linkSlug){
            var loginView = new BlogView(linkSlug);
            loginView.render();
        },
        linkList: function(){
            var loginView = new BlogListView();
            loginView.render();
        },
        juba: function(jubaSlug){
            var loginView = new JubaView(jubaSlug);
            loginView.render();
        },
        jubaList: function(){
            var loginView = new JubaListView();
            loginView.render();
        },
        initialize: function() {
            var router = this,
                routes = [
                    [ /^.*$/, "index" ],
                    [ 'blog', "blogList" ],
                    [ 'blog/*slug', "blog" ],
                    [ 'juba', "jubaList" ],
                    [ 'juba/*slug', "juba" ],
                    [ 'link', "linkList" ],
                    [ 'link/*slug', "link" ]
                ];

            _.each(routes, function(route) {
                router.route.apply(router,route);
            });

            Backbone.history.start();
        }
    });

    return AppRouter;
});
