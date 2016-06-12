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