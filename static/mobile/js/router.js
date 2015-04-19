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
    'static/mobile/js/views/LinkView.js',
    'js/views/ListView',
    'text!/static/mobile/templates/list.mustache',
    'js/model/JubaModel'
],function($, _, Backbone, HomeView, BlogView, BlogListView, JubaView, JubaListView, LinkView, ListView, linkDetailTemplate, LinkCollection){
    var AppRouter = Backbone.Router.extend({
        index: function(){
            new HomeView();
        },
        blog: function(blogSlug){
            new BlogView(blogSlug);
        },
        blogList: function(){
            new BlogListView();
        },
        link: function(linkSlug){
            new LinkView(linkSlug);
        },
        linkList: function(){
            new ListView(LinkCollection, linkDetailTemplate);
        },
        juba: function(jubaSlug){
            new JubaView(jubaSlug);
        },
        jubaList: function(){
            new JubaListView();
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
