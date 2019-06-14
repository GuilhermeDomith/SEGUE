$(document).ready(function () {

    $(document).ready(()=>{
        if(!navigator.onLine)
            statusOffline()

        window.addEventListener('offline', function (e) {
            console.log('offline');
            statusOffline()
        });
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
            descricao: 'Conecte-se a internet para continuar usando os serviçoes do SEGUE',
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