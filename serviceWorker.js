//instalacion e interceptacion
var CACHE_NAME = 'my-site-cache-v1';
var urlsToCache = [
    '/',
    '/quienes_somos',
    '/proximamente',
    '/static/css/estilo.css',
    '/static/img/logo-floreria.png',
    '/static/img/flor1.jpg',
    '/static/img/flor2.jpg',
    '/static/img/flor3.jpg',
    '/static/img/senko-san-2.jpg',
    '/static/img/senko-san.jpg',
];

self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(

      fetch(event.request)
      .then((result)=>{
        return caches.open(CACHE_NAME)
        .then(function(c) {
          c.put(event.request.url, result.clone())
          return result;
        })
        
      })
      .catch(function(e){
          return caches.match(event.request)
      })
  

     
    );
});

//codigo para notificaciones push

importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-messaging.js');

var firebaseConfig = {
  apiKey: "AIzaSyDmRRka_BsH6q8DU8_maU-0lJ7AbFUNW4s",
  authDomain: "floreriauwu-34da6.firebaseapp.com",
  databaseURL: "https://floreriauwu-34da6.firebaseio.com",
  projectId: "floreriauwu-34da6",
  storageBucket: "floreriauwu-34da6.appspot.com",
  messagingSenderId: "983352769456",
  appId: "1:983352769456:web:78ca654b00bcd1002c3475"
};
 //Initialize Firebase
firebase.initializeApp(firebaseConfig);

let messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload){

    let title = payload.Notification.title;

    let options = {
        body:payload.navigation.body,
        icon:payload.navigation.icon
    }

    self.registration.showNotification(title, options);

});