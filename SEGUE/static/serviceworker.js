const VERSAO = 3.5

const CACHE_ESTATICO = `SEGUE_ES_v${VERSAO}`
const CACHE_DINAMICO = `SEGUE_DI_v${VERSAO}`
const LAST_CACHE_ESTATICO = `SEGUE_ES_v${VERSAO-0.1}`
const LAST_CACHE_DINAMICO = `SEGUE_DI_v${VERSAO-0.1}`

const FILES_TO_CACHE = [
  '/',
  '/login/',
  '/offline/',

  'https://fonts.googleapis.com/css?family=Roboto:300,400,700,900',
  'https://fonts.googleapis.com/icon?family=Material+Icons',
  'https://fonts.googleapis.com/css?family=Varela+Round',


  '/static/js/base.js',
  '/static/js/config_ajax.js',
  '/static/js/jquery.min.js',
  '/static/js/materialize.min.js',
  '/static/js/wow.min.js',
  
  '/static/css/animate.css',
  '/static/css/base.css',
  '/static/css/materialize.min.css',

  '/static/icons/favicon.ico',
  '/static/icons/icon-128x128.png',
  '/static/icons/icon-144x144.png',
  '/static/icons/icon-152x152.png',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-256x256.png',
  '/static/icons/icon-512x512.png',

  '/static/logo/segue-bp.png',
  '/static/logo/segue-bp.svg',
  '/static/logo/segue-cor.png',
  '/static/logo/segue-cor.svg',
  '/static/logo/segue-pb.png',
  '/static/logo/segue-pb.svg',

  '/static/img/icon-github.svg',
  '/static/img/icon-lattes.png',
  '/static/img/icon-linkedin.svg',
  '/static/img/seta-pb.svg',
  '/static/img/seta.svg',
]


/** Armazenar os ativos da página em cache */
self.addEventListener('install', function(event) {
  this.skipWaiting(); /* */

  event.waitUntil(
    caches.open(CACHE_ESTATICO)
    .then(function(cache) {
        cache.addAll(FILES_TO_CACHE)
        .then(()=>{console.log('DONE: Todas as páginas de FILE_TO_CACHE foram salvas em cache')})
        .catch((e)=>{console.log('ERROR: As páginas de FILE_TO_CACHE não foram salvas em cache', e)})
    }).catch(function(err){
      console.log('Erro ao acessar cache',err)
    })
  );
});


self.addEventListener('fetch', function(event) {
  console.log('[SW] Fetch {'+event.request.url+'}');
  console.log('mode: ', event.request.mode !== 'navigate')

  // Se na url possui o endereço da nossa API de informações dinâmicas, não guardar no cache
  // No index.html possui um link para o service worker. Ele precisa estar explícito nesta lista
  // de exclusão, pois ao ser clicado ele não pode ser adicionado em cache.
  if(event.request.url.indexOf('serviceworker.js') > -1 ||
    event.request.url.indexOf('manifest.json') > -1){
    console.log('[SW] Fetch {Esta página não pode ser adicionada em cache}');

    event.respondWith(
      fetch(event.request)
      .catch((e)=>{console.log('Falha ao fazer requisição de {'+event.request.url+'}')})
    )
  }else{

    // Primeiro verifica se o item está no cache.
    // Em caso positivo apenas retorna.
    // Caso o item não exista no cache o item é obtido e em seguida salvo em cache
    event.respondWith(
      caches.match(event.request)
        .then(function(res){
          if(res){ // Se a variável for verdadeira, o item já estava no cache. Apenas retorna.
            console.log('[SW] Fetch (Pág. Cache) {'+event.request.url+'}');
            return res
          }else{
            // Faz a requisição e em seguida armazena o item em cache
            return fetch(event.request)
              .then(function(res){

                return caches.open(CACHE_DINAMICO) // Abre ou cria um cache com o nome fornecido
                  .then(function(cache){
                    // Atenção ao valor obtido pela requisição, que só pode ser utilizada uma vez
                    // Caso necessário sempre clonar a variável
                    // Método cache.put: Utilizado quando já se tem a url e a resposta
                    cache.put(event.request.url, res.clone())
                    console.log('[SW] Fetch (From Request, Stored on Cache) {'+event.request.url+'}');
                    return res
                  })
              })
              .catch(function(){
                // Retorna a página que informa o status offline
                return caches.match('/offline/')
              })
          }

        })
    );
  }

});


// Clear cache on activate
self.addEventListener('activate', event => {

  event.waitUntil( 
    caches.delete(LAST_CACHE_ESTATICO) &&
    caches.delete(LAST_CACHE_DINAMICO)
  )
});
  
