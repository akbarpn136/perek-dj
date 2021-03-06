/**
 * Created by sniper on 01/09/16.
 */

$(document).ready(function(){
    $("div#label_info").hide();
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
        resize: false,
        height : "480",
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

    $("a#tbl_butir").click(function(e){
        $("div#modal_butir").modal({
            closable  : false,
            onShow : function(){
                var selector = $("div#latar-samping");
                selector.css('min-height', selector.height()+28);
            }
        }).modal('show');

        e.preventDefault();
    });

    $("select#pilih_butir").dropdown({
        placeholder: true,
        fullTextSearch: 'exact',
        onChange: function(butir){
            var info = $("div#label_info");
            var keg = $("span#kegiatan").attr('data-value');

            $("input#butir").val(butir);

            $.get('/tugas/'+butir+'/butir/'+keg+'/', function(nilai){
                $("input#angka_hid").val(nilai['angka']);
                if(nilai['jenjang'] == '')
                {
                    info.text('Hasil: Data profil jenjang masih kosong, Harap diisi terlebih dahulu.');
                }

                else
                {
                    info.text('Hasil: '+nilai['hasil']+', Angka: '+nilai['angka']+' ('+nilai['persentase']+'% dari '+nilai['angka_asli']+')');
                }

                info.show();
            });
        }
    });

    $("a#tbl_nmr").click(function(e){
        var nomor = $('textarea#nomor');
        var baru = $("span#format").attr('data-value');

        baru = baru.replace('%nomor_urut%', '00')
            .replace('%kode_peran_pemberi%', $("span#kode_peran_pemberi").attr('data-value'))
            .replace('%kode_wbs_wp%', $("input#id_tingkatan").val())
            .replace('%kode_peran_penerima%', $("span#kode_peran_penerima").attr('data-value'))
            .replace('%kode_kegiatan%', $("span#kode_kegiatan").attr('data-value'))
            .replace('%bulan%', $("span#bulan").attr('data-value'))
            .replace('%tahun%', $("span#tahun").attr('data-value'));

        nomor.text();

        nomor.text(baru);
        e.preventDefault();
    });

    $("a#tbl_hapus").click(function(e){
        e.preventDefault();
        $("div#modal_hapus_keputusan").modal({
            closable  : false,
            onApprove : function(){
                $.get($("a#tbl_hapus").attr('data-value'), function(dt){
                    var html = '<a href="'+$("span#tbl_kembali").attr('data-value')+'" class="ui icon green button" title=" Kembali ke tugas ">';
                    html += '<i class="reply icon"></i> Kembali';
                    html += '</a>';

                    $("form").empty().prepend(dt).prepend(html);
                    var selector = $("div#latar-samping");
                    selector.css('min-height', '102%');
                });
            },
            onShow : function(){
                var selector = $("div#latar-samping");
                selector.css('min-height', selector.height()+28);
            }
        }).modal('show');
    });
});
