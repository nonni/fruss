/*
 * A simple jquery helper for pretty buttons 
 * adapted from http://www.monc.se/kitchen/59/scalable-css-buttons-using-png-and-background-colors#respond
 */
$(document).ready(function(){
    $('.btn').each(function(){
        var b = $(this);
        var tt = b.text() || b.val();
        if ($(':submit,:button',this)) {
            b = $('<a>').insertAfter(this). addClass(this.className).attr('id',this.id).attr('href',this.href);
            $(this).remove();
        }
        b.text('').css({cursor:'pointer'}). prepend('<i></i>').append($('<span>').
        text(tt).append('<i></i><span></span>'));
    });
});

