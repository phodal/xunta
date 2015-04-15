
var contents = function(html, tag) {
    if (html.indexOf('<' + tag + '>') >= 0) {
        return html.split('<' + tag + '>')[1].split('</' + tag + '>')[0];
    }
    return '';
};

var setRatingClick = function() {
    $('.arrows a').click(function() {

        var arrow = $(this);
        var index = arrow.find('i').hasClass('icon-arrow-up') ? 1 : 0;
        var container = arrow.parent().parent();
        var form = container.find('form');

        form.find('input:radio')[index].checked = true;

        $.post(form.attr('action'), form.serialize(), function(data) {
            if (data.location) {
                location = data.location;
            } else {
                //container.find('.score').text(data.rating_sum);
                $('.main').fadeTo(0, .5);
                $.get(location.href, {pjax: 1}, function(html) {
                    $('.main').fadeTo(0, 1);
                    var body = contents(html, 'body');
                    document.getElementsByTagName('body')[0].innerHTML = body;
                    setRatingClick();
                });
            }
        }, 'json');

        return false;
    });
};

$(setRatingClick);
