(function ($) {

var Models = {
    Author: Backbone.Model.extend({
        urlRoot: '/users/',
        defaults: {
            fullname: 'John Doe',
            username: 'someuser',
        },
    }),

    EntryTag: Backbone.Model.extend({
        defaults: {
            slug: 'invalid_slug',
            name: 'Unknown Tag',
            description: 'Not loaded',
        }
    }),

    Comment: Backbone.Model.extend({
        defaults: {
            id: -1,
            title: 'Unknown comment',
            content: 'No content.',
            author: 'Unknown author',
        }
    }),

    Entry: Backbone.Model.extend({
        defaults: {
            id: -1,
            slug: 'invalid_slug',
            title: 'No title',
            content: 'No content.',
            tags: [],
            created_on: new Date().toISOString(),
            modified_on: new Date().toISOString(),
            creator: '',
            comments: [],
        }
    }),
};

var Collections = {
    Authors: Backbone.Collection.extend({
        model: Models.Author
    }),

    Entries: Backbone.Collection.extend({
        model: Models.Entry,
        start_offset: 0,
        count: 10,
        comparator: function(entry) {
            return - new Date(entry.get('created_on')).valueOf();
        },
        url: function() {
            var ret = '/entries/latest?offset=' + this.start_offset + '&amp;count=' + this.count + '&amp;';
            return ret;
        },
    }),
};

var Views = {
    EntryAuthorView: Backbone.View.extend({
        template: Handlebars.compile($("#entryAuthorTemplate").html()),
        initialize: function() {
            this.model.on('change', this.render, this);
        },
        render: function() {
            console.log(this.model.toJSON(), 'rendering author');
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    }),

    EntryView: Backbone.View.extend({
        tagName: "article",
        className: "entry-container",
        template: Handlebars.compile($("#entryTemplate").html()),
        render: function() {
            var ctxt = this.model.toJSON();
            ctxt['created_timeago'] = $.timeago(ctxt['created_on']);
            console.log(ctxt, "Render entry");
            this.$el.html(this.template(ctxt));
            
            var author = new Models.Author({id: ctxt['creator']});
            author.fetch();
            var authorView = new Views.EntryAuthorView({
                el: this.$('#entry-author-'+ctxt['slug']),
                model: author
            });
            return this;
        }
    }),

    EntriesView: Backbone.View.extend({
        el: $("#entries"),
        initialize: function() {
            this.collection = new Collections.Entries();
            this.collection.fetch();
            this.render();
        },
        render: function() {
            var view_ctxt = this;
            _.each(this.collection.models, function(item) {
                view_ctxt.renderEntry(item);
            }, this);
        },
        renderEntry: function(entry) {
            var entryView = new Views.EntryView({
                model: entry,
            });
            this.$el.append(entryView.render().el);
        }
    }),
};

var entries_view = new Views.EntriesView();

} (jQuery));
