//instalacion e interceptacion
var CACHE_NAME = 'my-site-cache-v1';
var urlsToCache = [
    '/',
    '/static/core/css/estilos.css',
    '/static/core/img/logo.png',
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

//self.addEventListener('fetch', function(event) {
//    event.respondWith(
//        caches.match(event.request).then(function(response) {
//
//          return fetch(event.request)
//          .catch(function(rsp) {
//             return response; 
//          });
//          
//          
//        })
//    );
//});


//solo para cachear todo reemplazar por esta versión del Fetch


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
    apiKey: "AIzaSyA5cv5jrW8Cu8HToqhNm7rB3nWguZ3i_Jc",
    authDomain: "floreriauwu.firebaseapp.com",
    databaseURL: "https://floreriauwu.firebaseio.com",
    projectId: "floreriauwu",
    storageBucket: "floreriauwu.appspot.com",
    messagingSenderId: "1004657333762",
    appId: "1:1004657333762:web:9ba7dbb5f692e5f109b91b",
    measurementId: "G-13YHF7VVBD"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

let messaging = firebase.messaging();

messaging.setBackgroundMessageHandLer(function(payload){

    let title = payload.Notification.title;

    let options = {
        body:payload.navigation.body,
        icon:payload.navigation.icon
    }

    self.registration.showNotification(title, options);

});