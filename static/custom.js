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

    $("div.ui.fixed.menu").css('width', lebar_latar_samping);
    $("div#latar-samping").css('width', lebar_latar_samping).css('min-height', menu_samping_selector.height()+28);
    $('.ui.accordion').accordion({
        onOpen: function(){
            var selector = $("div#latar-samping");
            selector.css('min-height', $("div#kolom_samping").height()+28);
        }
    });

    if(menu_samping_selector.is(':hidden'))
    {
        $("body").css('padding-right', 0);
    }

    else
    {
        $("body").css('padding-right', 14);
    }

    $("div.ui.dropdown.little_menu").dropdown();
    $("div.ui.dropdown").dropdown();

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

    $("a#hapus_kategori").click(function(e){
        e.preventDefault();
        $("div#modal_hapus_kategori").modal({
            closable  : false,
            onApprove : function(){
                $.get($("a#hapus_kategori").attr('data-value'), function(dt){
                    var html = '<a href="/kategori/" class="ui icon green button" title=" Kembali ke kategori " style="position: absolute;top: -75px;right: -4px;">';
                    html += '<i class="reply icon"></i>';
                    html += '</a>';

                    $("form").empty().prepend(dt).prepend(html);
                    $("a#hapus_kategori").remove();
                });
            },
            onShow : function(){
                var selector = $("div#latar-samping");
                selector.css('min-height', selector.height()+28);
            }
        }).modal('show');
    });

    $("a#hapus_kegiatan").click(function(e){
        e.preventDefault();
        $("div#modal_hapus_kegiatan").modal({
            closable  : false,
            onApprove : function(){
                $.get($("a#hapus_kegiatan").attr('data-value'), function(dt){
                    var html = '<a href="/" class="ui icon green button" title=" Kembali ke utama " style="position: absolute;top: -75px;right: -4px;">';
                    html += '<i class="reply icon"></i>';
                    html += '</a>';

                    $("form").empty().prepend(dt).prepend(html);
                    $("a#hapus_kegiatan").remove();
                });
            },
            onShow : function(){
                var selector = $("div#latar-samping");
                selector.css('min-height', selector.height()+28);
            }
        }).modal('show');
    });

    $("a#hapus_format").click(function(e){
        e.preventDefault();
        $("div#modal_hapus_format").modal({
            closable  : false,
            onApprove : function(){
                $.get($("a#hapus_format").attr('data-value'), function(dt){
                    var html = '<a href="'+ $("a#tbl_kembali").attr('href') +'" class="ui icon green button" title=" Kembali ke utama " style="position: absolute;top: -75px;right: -4px;">';
                    html += '<i class="reply icon"></i>';
                    html += '</a>';

                    $("form").empty().prepend(dt).prepend(html);
                    $("a#hapus_format").remove();
                });
            },
            onShow : function(){
                var selector = $("div#latar-samping");
                selector.css('min-height', selector.height()+28);
            }
        }).modal('show');
    });

    $("a#hapus_personil").click(function(e){
        e.preventDefault();
        $("div#modal_hapus_personil").modal({
            closable  : false,
            onApprove : function(){
                $.get($("a#hapus_personil").attr('data-value'), function(dt){
                    var html = '<a href="'+ $("a#tbl_kembali").attr('href') +'" class="ui icon green button" title=" Kembali ke utama " style="position: absolute;top: -75px;right: -4px;">';
                    html += '<i class="reply icon"></i>';
                    html += '</a>';

                    $("form").empty().prepend(dt).prepend(html);
                    $("a#hapus_personil").remove();
                });
            },
            onShow : function(){
                var selector = $("div#latar-samping");
                selector.css('min-height', selector.height()+28);
            }
        }).modal('show');
    });

    $("a#tentang_aplikasi").click(function(e){
        e.preventDefault();
        $("div#modal_tentang_aplikasi").modal({
            closable  : false,
            onShow : function(){
                var selector = $("div#latar-samping");
                selector.css('min-height', selector.height()+28);
            }
        }).modal('show');
    });

    $("select#select_kategori_multi").dropdown();
    $("select#select_format").dropdown({
        placeholder: true
    });

    $("a.kode.header").click(function(e){
        e.preventDefault();
        var box = $("textarea#id_formasi");
        box.val(box.val() + $(this).text());
    });

    $(window).resize(function(){
        var lebar_latar_samping_selector = $(".three.wide.column");
        var lebar_latar_samping = lebar_latar_samping_selector.width();

        $("div#latar-samping").css('width', lebar_latar_samping_selector.width())
                                .css('min-height', menu_samping_selector.height()+28);
        $("div.ui.fixed.menu").css('width', lebar_latar_samping);

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