/**
 * Created by syariefa on 5/19/16.
 */

$(document).ready(function(){
    $(".message .close").click(function(){
        $(this).closest('.message').transition('fade');
    });

    var lebar_latar_samping_selector = $(".three.wide.column");
    var lebar_latar_samping = lebar_latar_samping_selector.width();
    var menu_samping_selector = $("div#kolom_samping");
    //var lebar_latar_samping_pad = lebar_latar_samping_selector.css('padding-right').replace("px", "");
    //var lebar_max = lebar_latar_samping;

    $("div#latar-samping").css('width', lebar_latar_samping).css('min-height', menu_samping_selector.height()+28);
    $('.ui.accordion').accordion();

    if(menu_samping_selector.is(':hidden'))
    {
        $("body").css('padding-right', 0);
    }

    else
    {
        $("body").css('padding-right', 14);
    }

    $("div.ui.dropdown.little_menu").dropdown();

    $.get("/json_kegiatan/", function(data){
        $('.ui.search').search({
            source: data,
            searchFields: ['title'],
            searchFullText: true,
            onSelect: function(result){
                window.location.replace('/cari/'+result['slug']+'/');
            }
        });
    });

    $('.prompt').keypress(function(e) {
        var slug = function(str) {
            var $slug = '';
            var trimmed = $.trim(str);
            $slug = trimmed.replace(/[^a-z0-9-]/gi, '-').
            replace(/-+/g, '-').
            replace(/^-|-$/g, '');
            return $slug.toLowerCase();
        };

        if(e.which == 13) {
            window.location.replace('/cari/'+slug($(this).val())+'/');
        }
    });

    $(window).resize(function(){
        $("div#latar-samping").css('width', lebar_latar_samping_selector.width())
                                .css('min-height', menu_samping_selector.height()+28);
        if(menu_samping_selector.is(':hidden'))
        {
            $("body").css('padding-right', 0);
        }

        else
        {
            $("body").css('padding-right', 14);
        }
    });
});