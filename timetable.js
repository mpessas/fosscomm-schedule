function get_template(row, speech) {
    row.find('.thour').html(speech.hour);
    row.find('.tb1').text(speech.title);
    row.find('.tb2').text(speech.speaker);
    return row;
}

$(function() {
    // Fetch data to begin with
    $.ajax({
        type: 'GET',
        url: 'fetch_data.json',
        timeout: 10000,
        dataType: 'json',
        error: function(xhr, status, error) {
            alert(status + ": " + error);
        },
        success: function(data) {
            alert(data.length);
            for (var i in data) {
                var newRow = $('.template').clone().removeClass('template');
                alert(data[i]);
                get_template(newRow, data[i]).appendTo('table');
            }
        }
    });
    // handle links to speeches
    $('td a').click(function(e) {
        // Support for js history API
        if (window.history && window.history.pushState) {
            e.preventDefault()
            var filename = this.id + ".json";
            var state = { "hidden": true };
            var title = "Speech: " + this.id;
            window.history.pushState(state, title);

            // load new data for selection
            var path = filename;
            $.ajax({
                type: 'GET',
                url: path,
                timeout: 10000,
                dataType: 'json',
                error: function(xhr, status, error) {
                    alert(status + " " + error);
                },
                success: function(data) {
                    $('#res').find('#title').text(data.title);
                    $('#res').find('#summary').text(data.summary);
                    $('#res').find('#speaker').text(data.speaker);
                    $('#res').find('#details').html(data.day + 
                                                    ", " + data.hour +
                                                    " @ " + data.room);
                    $('table').fadeOut('fast', function() {
                        $('#res').fadeIn('fast');
                    });
                }
            });

            // handle back button
            $(window).bind("popstate", function() {
                $('div#res').fadeOut('fast', function() {
                    $('table').fadeIn('slow');
                });
            });
        }
    });

    // Animate o mouseover
    $('td').hover(function() {
        $(this).animate({fontSize: '+=5px'}, 200);
    }, function() {
        $(this).animate({fontSize: '-=5px'}, 200);
    });
});
