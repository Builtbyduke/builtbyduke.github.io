(function(){
  var btn = document.getElementById('navToggle');
  var sidebar = document.getElementById('sidebar');
  if(!btn || !sidebar) return;
  btn.addEventListener('click', function(){
    var open = sidebar.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.addEventListener('click', function(e){
    if(window.innerWidth > 900) return;
    if(!sidebar.contains(e.target) && e.target !== btn && sidebar.classList.contains('open')){
      sidebar.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
    }
  });
})();
