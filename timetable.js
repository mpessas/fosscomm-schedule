// handle links to speeches
$(function() {
    $('td a').click(function() {
        $('table').hide();
        var file = this.id + ".json";
        if (window.history && window.history.pushState) {
            var title = "Speech: " + this.id;
            var path = "speech_" + this.id + ".html";
            alert("Supported! " + title + " " + path);
            window.history.pushState({
                hidden: true
            }, title, path);
        }
    });
});
