const CACHE_ESTATICO = 'SEGUE_ES_v1.3';
const CACHE_DINAMICO = 'SEGUE_DI_v1';
const FILES_TO_CACHE = [
  '/',
  '/base_layout',
  '/login',

  'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js',
  'https://fonts.googleapis.com/css?family=Roboto:300,400,700,900',
  'https://fonts.googleapis.com/icon?family=Material+Icons',

  'static/js/base.js',
  'static/js/config_ajax.js',
  '/static/css/base.css',
  '/static/css/materialize.min.css',
  '/static/img/favicon.ico',
]


/** Armazenar os ativos da página em cache */
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_ESTATICO)
    .then(function(cache) {
        cache.addAll(FILES_TO_CACHE);
    }).catch(function(err){
      console.log('Erro ao acessar cache',err)
    })
  );
});

self.addEventListener('fetch', function(event) {
  console.log('[SW] Fetch {'+event.request.url+'}');

  // Se na url possui o endereço da nossa API de informações dinâmicas, não guardar no cache
  // No index.html possui um link para o service worker. Ele precisa estar explícito nesta lista
  // de exclusão, pois ao ser clicado ele não pode ser adicionado em cache.
  if(event.request.url.indexOf('serviceworker.js') > -1 ||
    event.request.url.indexOf('manifest.json') > -1){

    event.respondWith(fetch(event.request))
  }else{

    // Primeiro verifica se o item está no cache.
    // Em caso positivo apenas retorna.
    // Caso o item não exista no cache o item é obtido e em seguida salvo em cache
    event.respondWith(
      caches.match(event.request)
        .then(function(res){
          if(res){ // Se a variável for verdadeira, o item já estava no cache. Apenas retorna.
            console.log('[SW] Fetch (Cache) {'+event.request.url+'}');
            return res
          }
          else{
            // Faz a requisição e em seguida armazena o item em cache
            return fetch(event.request)
              .then(function(res){

                return caches.open(CACHE_DINAMICO) // Abre ou cria um cache com o nome fornecido
                  .then(function(cache){
                    // Atenção ao valor obtido pela requisição, que só pode ser utilizada uma vez
                    // Caso necessário sempre clonar a variável
                    // Método cache.put: Utilizado quando já se tem a url e a resposta
                    cache.put(event.request.url,res.clone())
                    console.log('[SW] Fetch (Request|Cache) {'+event.request.url+'}');
                    return res
                  })
              })
          }
        })
    );
  }

});