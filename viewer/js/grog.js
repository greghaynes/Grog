(function ($) {

// Stub content for testing
var stub_tags = [
    { slug: 'tag1', name: 'Tag 1' },
    { slug: 'tag2', name: 'Tag 2' }
];

var stub_entries = [
    {
        id: 0,
        slug: 'the_first_entry',
        title: "The First Entry",
        content: "This is the first entry, not a lot to <b>see</b> here.", 
        tags: [stub_tags[0]],
        creator: 'testuser',
        created_on: "2008-07-17T09:24:17Z",
        modified_on: "2008-07-17T09:24:17Z",
    }, {
        id: 1,
        slug: 'second_entry',
        title: "A Second Entry",
        content: "This is the second entry. There is not a lot to <b>see</b> here.", 
        tags: [stub_tags[0], stub_tags[1]],
        creator: 'testuser',
        comments: [
            {
                title: 'Comment one',
                content: 'This it comment number one',
                author: 'Some person'
            },
        ],
    },
];

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
        comparator: function(entry) {
            return - new Date(entry.get('created_on')).valueOf();
        }
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
            this.collection = new Collections.Entries(stub_entries);
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
