// Advanced Search filter panel: status / standard type / publisher / edition
// / validity / dependency-graph facets, composed with the free-text query by
// RulesSearch.search(query, {filters}). Field:value typed tokens (see
// search.js parseAdvanced) work without this panel; this just gives the same
// mechanism a discoverable UI.
window.RulesAdvancedSearch = (function () {
  const DB = window.RulesDB;
  const STATUS_OPTIONS = ['current', 'superseded', 'repealed', 'withdrawn', 'draft', 'future-effective'];
  const TYPE_OPTIONS = ['convention', 'code', 'rule', 'act', 'circular', 'resolution', 'order', 'notice'];

  let onChange = null;

  function populate() {
    const statusSel = document.getElementById('adv-status');
    const typeSel = document.getElementById('adv-type');
    const pubSel = document.getElementById('adv-publisher');
    const validitySel = document.getElementById('adv-validity');
    if (!statusSel || statusSel._populated) return;
    statusSel._populated = true;

    statusSel.innerHTML = '<option value="">Any status</option>' + STATUS_OPTIONS.map((s) => `<option value="${s}">${s}</option>`).join('');
    typeSel.innerHTML = '<option value="">Any type</option>' + TYPE_OPTIONS.map((t) => `<option value="${t}">${t}</option>`).join('');
    const orgs = DB.getOrganizations();
    pubSel.innerHTML = '<option value="">Any organization</option>' + Object.keys(orgs).map((id) => `<option value="${id}">${orgs[id].name}</option>`).join('');
    validitySel.innerHTML = '<option value="">Any validity</option><option value="has">Has structured validity</option><option value="missing">Missing validity metadata</option>';

    ['adv-status', 'adv-type', 'adv-publisher', 'adv-validity', 'adv-edition', 'adv-depends'].forEach((id) => {
      document.getElementById(id).addEventListener(id === 'adv-edition' || id === 'adv-depends' ? 'input' : 'change', () => { if (onChange) onChange(); });
    });
    document.getElementById('adv-clear').addEventListener('click', () => {
      statusSel.value = ''; typeSel.value = ''; pubSel.value = ''; validitySel.value = '';
      document.getElementById('adv-edition').value = ''; document.getElementById('adv-depends').value = '';
      if (onChange) onChange();
    });
    document.getElementById('adv-toggle').addEventListener('click', () => {
      document.getElementById('adv-panel').classList.toggle('open');
    });
  }

  function getFilters() {
    const val = (id) => { const el = document.getElementById(id); return el && el.value ? el.value.toLowerCase() : ''; };
    const filters = {};
    if (val('adv-status')) filters.status = val('adv-status');
    if (val('adv-type')) filters.type = val('adv-type');
    if (val('adv-publisher')) filters.publisher = val('adv-publisher');
    if (val('adv-validity')) filters.validity = val('adv-validity');
    if (val('adv-edition')) filters.edition = val('adv-edition');
    if (val('adv-depends')) filters.depends = val('adv-depends');
    return filters;
  }

  function init(changeCallback) {
    onChange = changeCallback;
    populate();
  }

  return { init, getFilters };
})();
