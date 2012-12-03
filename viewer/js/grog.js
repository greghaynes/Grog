(function ($) {

var Models = {
    User: Backbone.Model.extend({
        urlRoot: '/api/users/',
        defaults: {
            fullname: 'John Doe',
        },
        browseurl: function() {
            return '/users/' + this.id;
        }
    }),

    Comment: Backbone.Model.extend({
        defaults: {
            id: -1,
            title: 'Unknown comment',
            content: 'No content.',
            author: 'undefined_author',
        }
    }),

    Entry: Backbone.Model.extend({
        defaults: {
            id: -1,
            slug: 'invalid_slug',
            title: 'No title',
            content: 'No content.',
            created_on: new Date().toISOString(),
            modified_on: new Date().toISOString(),
            creator: '',
        },
        initialize: function() {
            this.comments = new Collections.EntryComments;
            this.comments.url = '/api/entries/' + this.get('slug') + '/comments';
            this.comments.fetch();
        }
    }),
};

var Collections = {
    EntryComments: Backbone.Collection.extend({
        model: Models.Comment,
    }),

    Entries: Backbone.Collection.extend({
        model: Models.Entry,
        start_offset: 0,
        count: 10,
        comparator: function(entry) {
            return - new Date(entry.get('created_on')).valueOf();
        },
        url: function() {
            return '/api/entries/latest';
            //?offset=' + this.start_offset + '&amp;count=' + this.count + '&amp;';
        },
    }),
};

var Views = {
    EntryCommentsView: Backbone.View.extend({
        blurb_template: Handlebars.compile($("#entryCommentsBlurbTemplate").html()),
        full_template: Handlebars.compile($("#entryCommentsTemplate").html()),
        initialize: function() {
            this.model.on("reset", this.render, this);
        },
        render: function() {
            var ctxt = this.model.toJSON();
            console.log(ctxt, "rendering comments");
            this.$el.html(this.blurb_template({ comments: ctxt }));
            return this;
        }
    }),

    EntryAuthorView: Backbone.View.extend({
        template: Handlebars.compile($("#entryAuthorTemplate").html()),
        initialize: function() {
            this.model.on('change', this.render, this);
        },
        render: function() {
            var ctxt = this.model.toJSON();
            ctxt['browseurl'] = this.model.browseurl();
            console.log(ctxt, 'rendering author');
            this.$el.html(this.template(ctxt));
            return this;
        }
    }),

    EntryView: Backbone.View.extend({
        tagName: "article",
        className: "entry-container",
        template: Handlebars.compile($("#entryTemplate").html()),
        initialize: function() {
            this.model.on('reset', this.render, this);
        },
        render: function() {
            var ctxt = this.model.toJSON();
            ctxt['created_timeago'] = $.timeago(ctxt['created_on']);
            ctxt['editable'] = my_user.get('username') == this.model.get('creator');
            console.log(ctxt, "Render entry");
            this.$el.html(this.template(ctxt));
            
            this.renderAuthor(ctxt['creator'], this.$("#entry-author-" + ctxt['slug']));
            console.log(this.model.comments.toJSON(), 'entry comments');

            var comments_view = new Views.EntryCommentsView({
                el: this.$("#entry-comments-"+ctxt['slug']),
                model: this.model.comments
            });
            comments_view.render();
            return this;
        },

        renderAuthor: function(username, target_el) {
            var author = new Models.User({id: username});
            var authorView = new Views.EntryAuthorView({
                el: target_el,
                model: author
            });
            author.fetch();
        }
    }),

    EntriesView: Backbone.View.extend({
        el: $("#entries"),
        initialize: function() {
            this.collection = new Collections.Entries();
            this.collection.on('add', this.render, this);
            this.collection.on('reset', this.render, this);
            this.collection.fetch();
            this.render();
        },
        render: function() {
            _.each(this.collection.models, function(item) {
                this.renderEntry(item);
            }, this);
            return this;
        },
        renderEntry: function(entry) {
            var entryView = new Views.EntryView({
                model: entry,
            });
            this.$el.append(entryView.render().el);
        },
        onAdded: function(model, collection) {
            console.log(entry, 'entry added');
        },
    }),
};

var my_user = new Models.User({ id: 'me' });
my_user.fetch();

var entries_view = new Views.EntriesView();

} (jQuery));
