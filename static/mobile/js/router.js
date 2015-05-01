"use strict";

define([
    'jquery',
    'underscore',
    'backbone',
    'js/views/HomeView',
    'js/views/BasicPageView',
    'js/views/ListPageView',
    'text!templates/list.mustache',
    'text!templates/detail.mustache',
    'js/model/ListModel'
],function($, _, Backbone, HomeView, BasicPageView, ListPageView, listTemplate, detailTemplate, ListCollection){
    var AppRouter = Backbone.Router.extend({
        index: function(){
            new HomeView();
        },
        blog: function(blogSlug){
            new BasicPageView(new ListCollection('/api/blog_detail/'), detailTemplate, 'blog', {slug: blogSlug});
        },
        blogList: function(){
            new ListPageView(new ListCollection('/api/blog_list/'), listTemplate, 'blog');
        },
        link: function(linkSlug){
            new BasicPageView(new ListCollection('/api/link_detail/'), detailTemplate, 'link', {slug: linkSlug});
        },
        linkList: function(){
            new ListPageView(new ListCollection('/api/link_list/'), listTemplate, 'link');
        },
        juba: function(jubaSlug){
            new BasicPageView(new ListCollection('/api/juba_detail/'), detailTemplate, 'juba', {slug: jubaSlug});
        },
        jubaList: function(){
            new ListPageView(new ListCollection('/api/juba_list/'), listTemplate, 'juba');
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
