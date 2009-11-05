$(document).ready( function() {
$('*[id^=read]').click( function() {
        var id = this.id.substr(5);
        $.ajax({
            type: "GET",
            url: '/forum/set_read/'+id+'/',
            success: function(data){
                $('#thread_'+id).attr('class', $('#thread_'+id).attr('class').substr(6));
                $('#read_'+id).html('');
            }
        });
    });
});
