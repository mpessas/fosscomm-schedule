// window.onpopstate = function(event) {
//     if (event.state.hidden) {
//         document.getElementById('schedule').display = 'inherit'
//     }
// }

// handle links to speeches
$(function() {
    $('td a').click(function() {
        $('table').hide()
        var file = this.id + ".json"
        var stateObj = {hidden: true}
        history.pushState(stateObj, "Speech: " + this.id, "speech/" + file)
        
    });
});
