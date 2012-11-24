(function ($) {

// Stub content for testing
var stub_contacts = [
    { fullname: "Fred Fredderson", username: 'fredf' },
];

var stub_entries = [
    {
        slug: 'the_first_entry',
        title: "The First Entry",
        content: "This is the first entry, not a lot to <b>see</b> here.", 
        tags: ['Tag1'],
        creator: stub_contacts[0],
        created_on: "2008-07-17T09:24:17Z",
        modified_on: "2008-07-17T09:24:17Z",
    }, {
        slug: 'second_entry',
        title: "A Second Entry",
        content: "This is the second entry. There is not a lot to <b>see</b> here.", 
        tags: ['Tag1', 'Tag2'],
        creator: stub_contacts[0],
    },
];

var Author = Backbone.Model.extend({
    defaults: {
        fullname: 'John Doe',
        username: 'someuser',
    }
})

var Entry = Backbone.Model.extend({
    defaults: {
        slug: 'invalid_slug',
        title: 'No title',
        content: 'No content.',
        tags: [],
        created_on: new Date().toISOString(),
        modified_on: new Date().toISOString(),
        creator: new Author(),
    }
});

var Entries = Backbone.Collection.extend({
    model: Entry
});

var EntryView = Backbone.View.extend({
    tagName: "article",
    className: "entry-container",
    template: Handlebars.compile($("#entryTemplate").html()),
    render: function() {
        var ctxt = this.model.toJSON();
        ctxt['created_timeago'] = $.timeago(ctxt['created_on']);
        console.log(ctxt, "Render entry");
        this.$el.html(this.template(ctxt));
        return this;
    }
});

var EntriesView = Backbone.View.extend({
    el: $("#entries"),
    initialize: function() {
        this.collection = new Entries(stub_entries);
        this.render();
    },
    render: function() {
        var view_ctxt = this;
        _.each(this.collection.models, function(item) {
            view_ctxt.renderEntry(item);
        }, this);
    },
    renderEntry: function(entry) {
        var entryView = new EntryView({
            model: entry,
        });
        this.$el.append(entryView.render().el);
    }
});

var entries_view = new EntriesView();

} (jQuery));
