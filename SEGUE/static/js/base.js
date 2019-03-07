$(document).ready(function () {

    /* Configura os componentes do Materialize*/
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.dropdown-trigger').dropdown();
    $('.modal').modal();
    $('select').formSelect();

    var options_datepicker = {
        format: 'dd/mm/yyyy',
        i18n: {
            cancel:	'Cancelar',
            clear: 'Limpar',
            done: 'Ok',
            months:[
                'Janeiro', 'Fevereiro', 'Março',
                'Abril', 'Maio', 'Junho',
                'Julho', 'Agosto', 'Setembro',
                'Outubro', 'Novembro', 'Dezembro'
            ],
            monthsShort: [
                'Jan', 'Fev', 'Mar',
                'Abr', 'Mai', 'Jun',
                'Jul', 'Ago', 'Set',
                'Out', 'Nov', 'Dez'
            ],                   
            weekdays: [
                'Domingo', 'Segunda', 'Terça', 'Quarta',
                'Quinta', 'Sexta', 'Sábado'
            ],
            weekdaysShort: [
                'Dom', 'Seg', 'Ter', 'Qua',
                'Qui', 'Sex', 'Sab'
            ],
            weekdaysAbbrev:	['D','S','T','Q','Q','S','S']
        }};
        
    $('.datepicker').datepicker(options_datepicker);

    /* Permite alterar a opção selecionada em um select. */
    function select_value_selector(selector, value) {
        let option = selector.find('option[value='+ value+']')

        selector.val(value)
            .closest('.select-wrapper')
            .find('li')
            .removeClass("active")
            .closest('.select-wrapper')
            .find('.select-dropdown')
            .val(option.html())
            .find('span:contains(' + option.html() + ')')
            .parent().addClass('selected active');
    }

    /* Obtém todos os select da página e seleciona a opção marcada em data-select.*/
    $('select').each((i, select)=>{
        let data_select = $(select).attr('data-select')
        if(data_select != '')
            select_value_selector($(select), data_select)
    })

    /* Obtém todos os grupos de Radio Button e seleciona um radio button de 
    acordo com o atributo data-select do grupo. Se data-select for vazio 
    seleciona o primeiro radio button*/
    $('.group-radio-button').each((i, group)=>{
        group = $(group)
        let id_select = group.attr('data-select');
        let radio = group.find('input')[0];

        if (id_select != '')
            radio = group.find('input[value=' + id_select + ']')[0];

        radio.checked = true;
    });

});