// handle links to speeches
$(function() {
    $('td a').click(function(e) {
        if (window.history && window.history.pushState) {
            e.preventDefault()
            $('table').hide();
            var file = this.id + ".json";
            var state = { "hidden": true };
            var title = "Speech: " + this.id;
            window.history.pushState(state, title);
        }
    });
});
