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

  // Swan script
  !function(){
    var w = window;
    var swan = (w.swan = w.swan || []);
    if (swan.isLoaded) return;
    swan.isLoaded = true;
    swan.pk = 'cm9gruwlf0012lg05hqu0s4ih';
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.async = true;
    script.src = 'https://swan-scripts.s3.amazonaws.com/bundle.js';
    var head = document.getElementsByTagName('head')[0];
    head.appendChild(script);
  }();
})(); 