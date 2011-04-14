function get_template(row, speech, selection) {
    var checked = selection[speech.id - 1] ? 'checked="checked"' : '';
    var speechHtml = '<a href="/api/schedule/presentation/' + speech.id +
        '" id="' + speech.id + '">' +
        speech.title + '</a>';
    if (speech.room == "Β1") {
        row.find('.tb1hour').html(speech.time_start + " &#150 " + speech.time_end);
        row.find('.tb1speech').html(speechHtml);
        row.find('.tb1speaker').text(speech.speaker);
        var chbox = "<input type='checkbox' id='chbox" + speech.id + 
            "' value='" + speech.id + "' " + checked +  "/>Ναι";
        row.find('.tb1attend').html(chbox);
    } else if (speech.room == "Β4") {
        row.find('.tb4hour').html(speech.time_start + " &#150 " + speech.time_end);
        row.find('.tb4speech').html(speechHtml);
        row.find('.tb4speaker').text(speech.speaker);
        var chbox = "<input type='checkbox' id='chbox" + speech.id + 
            "' value='" + speech.id + "' " + checked + "/>Ναι";
        row.find('.tb4attend').html(chbox);
    }
    return row;
}

function populate_table(day, data, selection) {
    $('table tbody').find('tr').not('.b1template, .b4template').remove();
    for (var i in data) {
        if (data[i].day == day) {
            if (data[i].room == "Β1") {
                var newRow = $('.b1template').clone().removeClass('b1template');
                get_template(newRow, data[i], selection).appendTo('table#schedule_b1');
            } else if (data[i].room == "Β4") {
                var newRow = $('.b4template').clone().removeClass('b4template');
                get_template(newRow, data[i], selection).appendTo('table#schedule_b4');
            }
        }
    }
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
            g_data = data;      // Save in global variable to access in links
            g_selection = Array(data.length);   // global event selection
            populate_table(1, data, g_selection);
        }
    });

    // handle links to speeches
    $('td a').live('click', function(e) {
        // Support for js history API
        if (window.history && window.history.pushState) {
            e.preventDefault()
            var filename = this.id;
            var title = "Speech: " + this.id;
            var url = "/api/schedule/presentation/" + this.id;
            window.history.pushState({}, title, url);
            
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
                if (document.location.pathname == "/schedule/schedule.html") {
                    $('#res').fadeOut('fast', function() {
                        $('#page1').fadeIn('slow');
                    });
                } else {
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
        var j = 0;
        for (var i in g_selection) {
            if (g_selection[i]) {
                checked[j] = parseInt(i) + 1;
                j++;
            }
        }
        window.open('/api/schedule/fosscomm.ical?events=' + checked.join(':'));
    });

    $('#register_form').submit(function(e) {
        var checked = [];
        var j = 0;
        for (var i in g_selection) {
            if (g_selection[i]) {
                checked[j] = parseInt(i) + 1;
                j++;
            }
        }
        console.log(checked);
        // Send selection to server
        $.ajax({
            type: 'POST',
            url: '/api/schedule/register/',
            timeout: 10000,
            dataType: 'json',
            data: {'events': checked.join(':'), 'jid_input': $('#jid_input').val()},
            error: function(xhr, status, error) {
                alert(status + ": " + error);
            },
            success: function(data) {
                alert("Registered successfully");
            }
        });
        return false;
    });

    // disable events on check/ enable on uncheck
    $('input').live('click', function(e) {
        // Add/remove from selection
        if (this.checked) {
            g_selection[this.id.substr(5) - 1] = true;
        } else {
            g_selection[this.id.substr(5) - 1] = false;
        }

        for (var i in g_data) {
            if (g_data[i].id == this.id.substr(5)) {
                var conflict = g_data[i].conflicts_with;
                for (var chbox in conflict) {
                    var chboxid = '#chbox' + conflict[chbox];
                    if (this.checked) {
                        $(chboxid).attr('disabled', true);
                    } else {
                        $(chboxid).removeAttr('disabled');
                    }
                }
            }
        }
    });

    // change day shown
    $('#day1').click(function(e) {
        e.preventDefault();
        populate_table(1, g_data, g_selection);
    });
    $('#day2').click(function(e) {
        e.preventDefault();
        populate_table(2, g_data, g_selection);
    });
});
