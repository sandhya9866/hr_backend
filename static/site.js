$(".menu-vertical li a").each(function () {
    if (window.location.pathname === $(this).attr('href')) {
        $(this).parent().parent().parent().addClass('active open');
        $(this).parent().addClass('active');
    }
});

// get anchor tag insode all .breadcrumb get text from anchor tag split it by _ and join it with space and capitalize first letter
$(".breadcrumb-item").each(function () {
    var text = $(this).find('a').text().split('_');
    text = text.map(function (item) {
        return item.charAt(0).toUpperCase() + item.slice(1);
    });
    text = text.join(' ');
    $(this).find('a').text(text);
});