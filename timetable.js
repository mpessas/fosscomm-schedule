$(function() {
    // handle links to speeches
    $('td a').click(function(e) {
        // Support for js history API
        if (window.history && window.history.pushState) {
            e.preventDefault()
            $('table').hide();
            var file = this.id + ".json";
            var state = { "hidden": true };
            var title = "Speech: " + this.id;
            window.history.pushState(state, title);

            // handle back button
            $(window).bind("popstate", function() {
                $('table').show();
            });
        }
    });
});
