function get_template(row, speech) {
    var speechHtml = '<a href="speech' + speech.id +
        '.html" id="' + speech.id + '">' +
        speech.title + '</a>';
    if (speech.room == "Β1") {
        row.find('.tb1hour').html(speech.time_start + " &#150 " + speech.time_end);
        row.find('.tb1speech').html(speechHtml);
        row.find('.tb1speaker').text(speech.speaker);
        var chbox = "<input type='checkbox' id='chbox" + speech.id + 
            "' value='" + speech.id + "' />Ναι";
        row.find('.tb1attend').html(chbox);
    } else if (speech.room == "Β4") {
        row.find('.tb4hour').html(speech.time_start + " &#150 " + speech.time_end);
        row.find('.tb4speech').html(speechHtml);
        row.find('.tb4speaker').text(speech.speaker);
        var chbox = "<input type='checkbox' id='chbox" + speech.id + 
            "' value='" + speech.id + "' />Ναι";
        row.find('.tb4attend').html(chbox);
    }
    return row;
}

$(function() {
    // JS enabled, hide warning
    $('#warning').hide()

    // Fetch data to begin with
    $.ajax({
        type: 'GET',
        url: '/api/schedule/',
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
            g_data = data;      // Save in global variable to access in links
        }
    });

    // handle links to speeches
    $('td a').live('click', function(e) {
        // Support for js history API
        if (window.history && window.history.pushState) {
            e.preventDefault()
            var filename = this.id;
            var state = { "hidden": true };
            var title = "Speech: " + this.id;
            var url = this.id + ".html";
            window.history.pushState(state, title, url);
            hidden = true;
            
            var data = g_data[this.id - 1];
            $('#res').find('#title').text(data.title);
            $('#res').find('#summary').text(data.summary);
            $('#res').find('#speaker').text(data.speaker);
            $('#res').find('#details').html(data.day + 
                                            ", " + data.time_start +
                                            " &#150 " + data.time_end +
                                            " @ " + data.room);
            $('#page1').fadeOut('fast', function() {
               $('#res').fadeIn('fast');
            });

            // handle back button
            $(window).bind("popstate", function(b) {
                if (hidden) {
                    hidden = false;
                    $('#res').fadeOut('fast', function() {
                        $('#page1').fadeIn('slow');
                    });
                } else {
                    hidden = true;
                    $('#page1').fadeOut('fast', function() {
                        $('#res').fadeIn('fast');
                    });
                }
            });
        }
    });

    // Animate on mouseover
    $('td').hover(function() {
        $(this).animate({fontSize: '+=5px'}, 200);
    }, function() {
        $(this).animate({fontSize: '-=5px'}, 200);
    });

    // Create ical file
    $('#ical').click(function(e) {
        e.preventDefault();
        var checked = [];
        $('input:checkbox:checked').each(function(i) {
            checked[i] = $(this).val();
        });
        console.log(checked)
        window.open('/api/schedule/fosscomm.ical?events=' + checked.join(':'));
    });

    // disable events on check/ enable on uncheck
    $('input').live('click', function(e) {
        for (var i in g_data) {
            if (g_data[i].id == this.id.substr(5)) {
                console.log(g_data[i].conflicts_with);
                var conflict = g_data[i].conflicts_with;
                for (var chbox in conflict) {
                    var chboxid = '#chbox' + conflict[chbox];
                    console.log(chboxid);
                    if (this.checked) {
                        $(chboxid).attr('disabled', true);
                    } else {
                        $(chboxid).removeAttr('disabled');
                    }
                }
            }
        }
    });
});
