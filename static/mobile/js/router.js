"use strict";

define([
    'jquery',
    'underscore',
    'backbone',
    'static/mobile/js/views/HomeView.js',
    'static/mobile/js/views/BlogView.js',
    'static/mobile/js/views/JubaView.js',
    'static/mobile/js/views/LinkView.js',
    'js/views/ListView',
    'text!/static/mobile/templates/list.mustache',
    'js/model/ListModel'
],function($, _, Backbone, HomeView, BlogView, JubaView, LinkView, ListView, linkDetailTemplate, LinkCollection){
    var AppRouter = Backbone.Router.extend({
        index: function(){
            new HomeView();
        },
        blog: function(blogSlug){
            new BlogView(blogSlug);
        },
        blogList: function(){
            new ListView(new LinkCollection('/api/blog_list/'), linkDetailTemplate, 'blog');
        },
        link: function(linkSlug){
            new LinkView(linkSlug);
        },
        linkList: function(){
            new ListView(new LinkCollection('/api/link_list/'), linkDetailTemplate, 'link');
        },
        juba: function(jubaSlug){
            new JubaView(jubaSlug);
        },
        jubaList: function(){
            new ListView(new LinkCollection('/api/juba_list/'), linkDetailTemplate, 'juba');
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
