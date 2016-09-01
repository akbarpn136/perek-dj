/**
 * Created by sniper on 01/09/16.
 */

$(document).ready(function(){
    $("input.tanggal").Zebra_DatePicker({
        show_icon: false,
        onSelect: function(a, b){
            var nilai_thn = b.slice(0, 4);
            var nilai_bln = b.slice(5, 7);

            $("span#bulan").attr('data-value', nilai_bln);
            $("span#tahun").attr('data-value', nilai_thn);
        },
        onClear: function(){
            $("span#bulan").attr('data-value', '');
            $("span#tahun").attr('data-value', '');
        }
    });

    tinymce.init({
        selector: 'textarea#isi',
        theme: 'modern',
        plugins: [
            'advlist autolink lists link image charmap print preview hr anchor pagebreak',
            'searchreplace wordcount visualblocks visualchars code fullscreen',
            'insertdatetime media nonbreaking save table contextmenu directionality',
            'emoticons template paste textcolor colorpicker textpattern imagetools'
        ],
        toolbar1: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
        toolbar2: 'print preview media | forecolor backcolor emoticons',
        image_advtab: true,
        setup : function(ed)
        {
            ed.on('init', function()
            {
                this.getDoc().body.style.fontSize = '14px';
                var selector = $("div#latar-samping");
                selector.css('min-height', $("div#kolom_konten").height()-$("div.ui.inverted.fixed.menu").height()+60);
            });
        }
    });

    $("select#select_orang").dropdown({
        placeholder: true,
        fullTextSearch: 'exact'
    });
});
