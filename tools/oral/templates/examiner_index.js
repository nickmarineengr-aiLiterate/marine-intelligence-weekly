function toggleSection(ex){
  var body = document.getElementById('body-'+ex);
  var sec = document.getElementById('ex-'+ex);
  var isOpen = body.style.display !== 'none';
  body.style.display = isOpen ? 'none' : 'block';
  sec.classList.toggle('open', !isOpen);
}
function openExaminer(ex){
  var body = document.getElementById('body-'+ex);
  var sec = document.getElementById('ex-'+ex);
  body.style.display = 'block';
  sec.classList.add('open');
}
function showBatch(ex, idx){
  document.querySelectorAll('.batch-panel[id^="batch-'+ex+'-"]').forEach(function(p){p.style.display='none';});
  document.getElementById('batch-'+ex+'-'+idx).style.display='block';
  document.querySelectorAll('.batch-tab[data-ex="'+ex+'"]').forEach(function(t){t.classList.remove('active');});
  document.querySelector('.batch-tab[data-ex="'+ex+'"][data-batch="'+idx+'"]').classList.add('active');
}
function filterTier(ex){
  var section = document.getElementById('ex-'+ex);
  var active = {};
  section.querySelectorAll('[data-tier-toggle]').forEach(function(cb){active[cb.dataset.tierToggle]=cb.checked;});
  section.querySelectorAll('.q-row').forEach(function(row){
    row.style.display = active[row.dataset.tier] ? '' : 'none';
  });
}
function filterSearch(term){
  term = term.toLowerCase().trim();
  document.querySelectorAll('.ex-section').forEach(function(sec){
    var anyMatch = false;
    sec.querySelectorAll('.q-row').forEach(function(row){
      var match = term==='' || row.textContent.toLowerCase().indexOf(term) !== -1;
      row.style.display = match ? '' : 'none';
      if(match) anyMatch = true;
    });
    if(term !== '' && anyMatch){
      document.getElementById('body-'+sec.id.replace('ex-','')).style.display='block';
      sec.classList.add('open');
      sec.querySelectorAll('.batch-panel').forEach(function(p){p.style.display='block';});
    }
  });
}
