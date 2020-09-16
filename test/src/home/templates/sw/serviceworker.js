var staticCacheName='voterable-cache'
var cached_pages = [
        '{% url "Home" %}'
        
        // I removed pollllist url here - i cannot comment it out as it will cause an error
        // '{% url "TagAllView" %}',
        // '{% url "like" %}',
        // '{% url "PollRecoView" %}',
        // '{% url "PollSuggView" %}',
        // '{% url "FAQ" %}',
        // '{% url "notifications_all" %}',
        // '{% url "AboutUs" %}',
        // '{% url "Contact" %}'


      ]

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      return cache.addAll(cached_pages);
    })
  );
});

// self.addEventListener('activate',function(event) {
//     event.waitUntil(
//     caches.keys().then(keys => Promise.all(
//       keys.map(key => {
//         if (!expectedCaches.includes(key)) return caches.delete(key);
//       })
//     ))
//   );
// });

// self.addEventListener('fetch', function(e) {
// //  console.log('[ServiceWorker] Fetch', e.request.url);
//   e.respondWith(
//     fetch(e.request).then(function(response){
//          caches.open(staticCacheName).then(function(cache) {
//               cache.addAll(cached_pages);
//           });
//          return response;
//         }
//       ).catch(function() {
//           return caches.match(e.request);
//        })
//   );
// });


self.addEventListener('fetch', function(e) {
//  console.log('[ServiceWorker] Fetch', e.request.url);
//  console.log('[ServiceWorker] Fetch', e.request.method);
  if(e.request.method == 'GET'){
      e.respondWith(
        fetch(e.request).then(function(response){
            var response2 = response.clone();
             caches.open(staticCacheName).then(function(cache) {
                  cache.match(e.request).then(function(r){
                        cache.put(e.request, response2);
                  });
              });
             return response;
            }
          ).catch(function() {
              return caches.match(e.request);
           })
      );
  }
});


importScripts('https://www.gstatic.com/firebasejs/4.8.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/4.8.1/firebase-messaging.js');
firebase.initializeApp({
    messagingSenderId: "{{SENDER_ID}}"
});

const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload) {

     console.log(payload);

//     var notificationTitle = 'Background Message Title';
//      var notificationOptions = {
//        body: 'Background Message body.',
//        icon: '/firebase-logo.png'
//      };

//      return self.registration.showNotification(notificationTitle,
//        notificationOptions);
});