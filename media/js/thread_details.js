$(document).ready( function() {
       $('*[id^=edit]').click( function() {            
            var id = this.id.substr(5);
            if( $(this).html() == "cancel" )
            {
                $.ajax({
                    type: "GET",
                    url: '/forum/get_post/'+id+'/',
                    success: function(data){
                        $('#post_'+id+'_body').html(data);
                    }
                });
                $(this).html("edit");
            }
            else
            {
                $.ajax({
                    type: "GET",
                    url: '/forum/edit_post/'+id+'/',
                    success: function(data){
                        $('#post_'+id+'_body').html(data);
                        $('#edit_submit_'+id).click(function() {
                            var form = $(this).parents('form:first');
                            var body = $("textarea[name='body']",form).val();
                            var markdown = $("input[name='markdown']:checked",form).val();
                            $.ajax({
                                type: "POST",
                                url: '/forum/edit_post/'+id+'/',
                                data: 'body='+body+'&markdown='+markdown,
                                success: function(data){
                                    $('#post_'+id+'_body').html(data);
                                    $('#edit_'+id).html('edit');
                                },
                                error: function(data){
                                    $('#post_'+id+'_body').html('Error received while editing post!');
                                }
                            });
                            return false;
                        });    
                    }
            });
            $(this).html("cancel");
        }
    });

    $('*[id^=hide]').click( function() {
        var id = this.id.substr(5);
        $.ajax({
            type: "GET",
            url: '/forum/hide_post/'+id+'/',
            success: function(data){
                $('#post_'+id).fadeOut('slow');
            }
        });
    });
});


