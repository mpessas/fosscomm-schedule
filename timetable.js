$(function() {
    // handle links to speeches
    $('td a').click(function(e) {
        // Support for js history API
        if (window.history && window.history.pushState) {
            e.preventDefault()
            $('table').hide();
            var filename = this.id + ".json";
            var state = { "hidden": true };
            var title = "Speech: " + this.id;
            window.history.pushState(state, title);

            // load new data for selection
            var path = filename;
            alert(path);
            $.ajax({
                type: 'GET',
                url: path,
                timeout: 10000,
                dataType: 'json',
                error: function(xhr, status, error) {
                    alert(status + " " + error);
                },
                success: function(data) {
                    var res = "<ul";
                    for (var p in data) {
                        res = res.concat("<li>", data[p], "</li>");
                    }
                    res += "</ul>";
                    $(res).appendTo('div#res');
                }
            });
            $('div#res').show();

            // handle back button
            $(window).bind("popstate", function() {
                $('table').show();
                $('div#res').hide();
            });
        }
    });
});
