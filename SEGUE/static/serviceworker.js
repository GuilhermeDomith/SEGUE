const VERSAO = 5.

const CACHE_ESTATICO = `SEGUE_ES_v${VERSAO}`
const CACHE_DINAMICO = `SEGUE_DI_v${VERSAO}`

const FILES_TO_CACHE = [
	'/',
	'/offline/',

	'https://fonts.googleapis.com/css?family=Roboto:300,400,700,900',
	'https://fonts.googleapis.com/icon?family=Material+Icons',
	'https://fonts.googleapis.com/css?family=Varela+Round',
	'https://fonts.gstatic.com/s/materialicons/v47/flUhRq6tzZclQEJ-Vdg-IuiaDsNcIhQ8tQ.woff2',
	'https://fonts.gstatic.com/s/varelaround/v11/w8gdH283Tvk__Lua32TysjIfp8uPLdshZg.woff2',
	'/static/admin/fonts/Roboto-Regular-webfont.woff',
	'/static/admin/img/sorting-icons.svg',

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
self.addEventListener('install', function (event) {
	this.skipWaiting();

	event.waitUntil(
		caches.open(CACHE_ESTATICO)
		.then(function (cache) {
			cache.addAll(FILES_TO_CACHE)
			.then(()=>{console.log('DONE: Os recursos estáticos foram salvos em cache')})
			.catch((err) => { console.log('ERROR: Os recursos estáticos não foram salvos em cache', e) })
		}).catch(function (err) {
			console.log(`ERROR: Não foi possível abrir o ${CACHE_ESTATICO}`, err);
		})
	);
});


self.addEventListener('fetch', function (event) {

	// Responde com o recurso que está em cache estático.
	// Se não, faz uma requisição e o salva em cache dinâmico.
	console.log('Irá atender requisição', event.request.url)
	event.respondWith(
		caches.open(CACHE_ESTATICO)
		.then((cache)=>{
			return cache.match(event.request).then((response)=>{
				if(response){
					console.log('Foi encontrado em cache estatico', event.request.url)
					return response
				}

				console.log('Nao está em cache estatico', event.request.url)
				return fetch(event.request).then((response) => {
						/* Salva recursos dinâmicas para acessa-los quando offline */

						//Recursos que não devem ser armazenados em cache
						if (event.request.url.indexOf('serviceworker.js') >= 0 ||
							event.request.url.indexOf('manifest.json') >= 0) {
							console.log('INFO: Conteúdo não pode ser armazenado em cache')
							return response
						}

						console.log('pag:', response.clone())

						console.log('O cache Dinamico vai ser feito', event.request.url)
						return caches.open(CACHE_DINAMICO).then(function (cache) {
							// Substitue a página em cache se já existe
							cache.put(event.request.url, response.clone())
							console.log(`UPDATE: Conteúdo atualizado em cache ${event.request.url}`);
							return response
						}).catch((err) => {
							console.log(`ERROR: Não foi possível abrir o ${CACHE_DINAMICO}`, err);
							return response
						})

				}).catch(e => {
					/* Erro ao fazer request */
					return caches.match('/')

					/* Cache dinâmico não utilizado

					//verifica se a página existe em cache dinamico
					return caches.match(event.request)
						.then((response) => {
							if(response) return response
							
							console.log('Nao está em cache Dinamico', event.request.url)
							// Retorna a página que informa o status offline
							return caches.match('/offline/')
						})
					*/
				})
			})
		})
	)
});


// Clear cache on activate
self.addEventListener('activate', event => {

	event.waitUntil(
		caches.keys()
		.then(cacheNames => {
			cacheNames.forEach(cachename =>{
				if(cachename !== CACHE_ESTATICO &&
					cachename !== CACHE_DINAMICO)
					caches.delete(cachename)
			})
		})
	)
});

