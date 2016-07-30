/**
 * Created by syariefa on 7/30/16.
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
                selector.css('min-height', $("div#kolom_samping").height()+28);
            });
        }
    });

    $("select#select_orang").dropdown({
        placeholder: true,
        fullTextSearch: 'exact',
        onChange: function(val){
            var keg = $("span#kegiatan").attr('data-value');

            $.get('/tugas/'+val+'/peran/'+keg+'/', function(prn){
                $("span#kode_peran_penerima").attr('data-value', prn[0]['peran']+prn[0]['wbs_wp_kode']+'.'+prn[0]['kode']);
            });
        }
    });

    $("a#tbl_nmr").click(function(e){
        var nomor = $('textarea#nomor');
        var baru = $("span#format").attr('data-value');

        baru = baru.replace('%nomor_urut%', '00')
            .replace('%kode_peran_pemberi%', $("span#kode_peran_pemberi").attr('data-value'))
            .replace('%kode_peran_penerima%', $("span#kode_peran_penerima").attr('data-value'))
            .replace('%kode_kegiatan%', $("span#kode_kegiatan").attr('data-value'))
            .replace('%bulan%', $("span#bulan").attr('data-value'))
            .replace('%tahun%', $("span#tahun").attr('data-value'));

        nomor.text();

        nomor.text(baru);
        e.preventDefault();
    });
});