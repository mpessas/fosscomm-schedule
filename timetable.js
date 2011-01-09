// handle links to speeches
$(function() {
    $('td a').click(function() {
        $('table').hide();
        var file = this.id + ".json";
        if (window.history && window.history.pushState) {
            var state = { "hidden": true };
            var title = "Speech: " + this.id;
            window.history.pushState(state, title);
        }
    });
});
