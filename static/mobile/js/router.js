"use strict";

define([
    'jquery',
    'underscore',
    'backbone',
    'js/views/HomeView',
    'js/views/ListView',
    'text!/static/mobile/templates/list.mustache',
    'text!/static/mobile/templates/detail.mustache',
    'js/model/ListModel'
],function($, _, Backbone, HomeView, ListView, listTemplate, detailTemplate, ListCollection){
    var AppRouter = Backbone.Router.extend({
        index: function(){
            new HomeView();
        },
        blog: function(blogSlug){
            new ListView(new ListCollection('/api/blog_detail/'), detailTemplate, 'blog', {slug: blogSlug});
        },
        blogList: function(){
            new ListView(new ListCollection('/api/blog_list/'), listTemplate, 'blog');
        },
        link: function(linkSlug){
            new ListView(new ListCollection('/api/link_detail/'), detailTemplate, 'link', {slug: linkSlug});
        },
        linkList: function(){
            new ListView(new ListCollection('/api/link_list/'), listTemplate, 'link');
        },
        juba: function(jubaSlug){
            new ListView(new ListCollection('/api/juba_detail/'), detailTemplate, 'juba', {slug: jubaSlug});
        },
        jubaList: function(){
            new ListView(new ListCollection('/api/juba_list/'), listTemplate, 'juba');
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
