// Analytics initialization
(function() {
  // Marketing suite
  !function(){
    const s = document.createElement('script');
    s.type = 'text/javascript';
    s.id = 'hs-script-loader';
    s.async = true;
    s.defer = true;
    s.src = '//js.hs-scripts.com/46490851.js';
    document.body.appendChild(s);
  }();

  // Visitor insights
  !function(){
    var reb2b = window.reb2b = window.reb2b || [];
    if (reb2b.invoked) return;
    reb2b.invoked = true;
    reb2b.methods = ["identify", "collect"];
    reb2b.factory = function(method) {
      return function() {
        var args = Array.prototype.slice.call(arguments);
        args.unshift(method);
        reb2b.push(args);
        return reb2b;
      };
    };
    for (var i = 0; i < reb2b.methods.length; i++) {
      var key = reb2b.methods[i];
      reb2b[key] = reb2b.factory(key);
    }
    reb2b.load = function(key) {
      var script = document.createElement("script");
      script.type = "text/javascript";
      script.async = true;
      script.src = "https://s3-us-west-2.amazonaws.com/b2bjsstore/b/" + key + "/EN4M0HKQZJOM.js.gz";
      var first = document.getElementsByTagName("script")[0];
      first.parentNode.insertBefore(script, first);
    };
    reb2b.SNIPPET_VERSION = "1.0.1";
    reb2b.load("EN4M0HKQZJOM");
  }();

  // User behavior tracking
  !function(s,n,i,t,c,h){
    s.SnitchObject=i;
    s[i]||(s[i]=function(){
      (s[i].q=s[i].q||[]).push(arguments)
    });
    s[i].l=+new Date;
    c=n.createElement(t);
    h=n.getElementsByTagName(t)[0];
    c.src='//snid.snitcher.com/8429711.js';
    h.parentNode.insertBefore(c,h)
  }(window,document,'snid','script');
  snid('verify', '8429711');

  // Engagement metrics
  !function(){
    const script = document.createElement('script');
    script.src = 'https://api.app.bullseye.so/api/v1/visitor-tracking/script/25fb5e2d-b7f4-4e78-8a84-63a7085f54d4';
    script.referrerPolicy = 'strict-origin-when-cross-origin';
    document.body.appendChild(script);
  }();
})(); 