$(document).ready(function () {
    // Verifica se o navegador está offline
    if(!navigator.onLine)
        setTimeout(statusOffline, 2000)

    window.addEventListener('offline', function (e) {
        console.log('offline');
        setTimeout(statusOffline, 2000)
    });


    let show_msg = JSON.parse( $('#show_msg').text() );
    
    if(show_msg != undefined && 
        show_msg.titulo != undefined &&
        show_msg.descricao != undefined)
        exibirMensagem({
            titulo: show_msg.titulo,
            descricao: show_msg.descricao,
            buttons: [{
                text: 'Ok',
                href: '#'
            }]
        })
})

function criarBotaoMensagem(button) {
    let btn = $('<a href="" class="modal-close waves-effect waves-red btn-flat"> </a>')
    btn.text(button.text)
    btn.attr('href', button.href)
    return btn
}

function statusOffline(){
    exibirMensagem({
            titulo: 'Você está offline',
            descricao: 'Conecte-se a internet para acessar o SEGUE',
            buttons: [{
                text: 'Ok',
                href: '#'
            }]
    })
}

function exibirMensagem(msg) {
    let botoes = []
    msg.buttons.forEach((obj) => {
        botoes.push(criarBotaoMensagem(obj))
    })

    $('#titulo-msg').text(msg.titulo)
    $('#descricao-msg').text(msg.descricao)
    $('#acoes-msg').empty().prepend(botoes)

    let modal = M.Modal.getInstance($('#mensagem'))
    modal.open();
}