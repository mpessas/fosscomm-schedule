function get_template(row, speech) {
    var speechHtml = '<a href="speech' + speech.id +
        '.html" id="speech' + speech.id + '">' +
        speech.title + '</a>';
    if (speech.room == "Β1") {
        row.find('.tb1hour').html(speech.hour);
        row.find('.tb1speech').html(speechHtml);
        row.find('.tb1speaker').text(speech.speaker);
    } else if (speech.room == "Β4") {
        row.find('.tb4hour').html(speech.hour);
        row.find('.tb4speech').html(speechHtml);
        row.find('.tb4speaker').text(speech.speaker);
    }
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
            for (var i in data) {
                if (data[i].room == "Β1") {
                    var newRow = $('.b1template').clone().removeClass('b1template');
                    get_template(newRow, data[i]).appendTo('table#schedule_b1');
                } else if (data[i].room == "Β4") {
                    var newRow = $('.b4template').clone().removeClass('b4template');
                    get_template(newRow, data[i]).appendTo('table#schedule_b4');
                }
            }
        }
    });
    // handle links to speeches
    $('td a').live('click', function(e) {
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
