(function ($) {

// Stub content for testing
var stub_contacts = [
    { fullname: "Fred Fredderson", username: 'fredf' },
];

var stub_entries = [
    {
        title: "The First Entry",
        content: "This is the first entry, not a lot to <b>see</b> here.", 
        creator: stub_contacts[0],
        created_on: moment().format(),
        modified_on: moment().format(),
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
        title: 'No title',
        content: 'No content.',
        created_on: moment().format(),
        modified_on: moment().format(),
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
        this.$el.html(this.template(this.model.toJSON()));
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
            model: entry
        });
        this.$el.append(entryView.render().el);
    }
});

var entries_view = new EntriesView();

} (jQuery));
