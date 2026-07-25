// Phase 2 Illustration Viewer: lightweight metadata loading, SVG modal viewer,
// placeholder card rendering, and bidirectional links to Engineering Objects,
// Definitions, and Regulations.
window.RulesIllustrations = (function () {
  const DB = window.RulesDB;
  const R = window.RulesRender;

  function openIllustrationModal(ill) {
    let existing = document.getElementById('ill-modal');
    if (existing) existing.remove();

    const modal = document.createElement('div');
    modal.id = 'ill-modal';
    modal.className = 'modal-backdrop';
    modal.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(15,23,42,0.85);z-index:9999;display:flex;align-items:center;justify-content:center;padding:20px;backdrop-filter:blur(6px);';

    const hasMedia = ill.mediaFile && !ill.mediaFile.endsWith('.gitkeep');
    const mediaUrl = hasMedia ? '../repository/' + ill.mediaFile : '';

    modal.innerHTML = `
      <div style="background:#fff;border-radius:12px;max-width:900px;width:100%;max-height:90vh;overflow-y:auto;box-shadow:0 20px 50px rgba(0,0,0,0.3);display:flex;flex-direction:column;">
        <div style="padding:16px 24px;background:var(--navy,#0f172a);color:#fff;display:flex;align-items:center;justify-content:space-between;border-radius:12px 12px 0 0;">
          <div>
            <h3 style="margin:0;font-size:18px;font-weight:700;">${R.esc(ill.title)}</h3>
            <span style="font-size:11px;color:var(--teal-light,#ccfbf1);text-transform:uppercase;letter-spacing:1px;font-weight:600;">${R.esc(ill.illustrationType)}</span>
          </div>
          <button type="button" id="close-ill-modal" style="background:none;border:none;color:#fff;font-size:24px;cursor:pointer;padding:0 8px;">&times;</button>
        </div>
        <div style="padding:24px;flex:1;">
          <div style="background:var(--grey-bg,#f1f5f9);border:1px dashed var(--grey-border,#e2e8f0);border-radius:8px;padding:30px;text-align:center;margin-bottom:20px;min-height:260px;display:flex;flex-direction:column;align-items:center;justify-content:center;">
            ${hasMedia
              ? `<img src="${R.esc(mediaUrl)}" alt="${R.esc(ill.title)}" style="max-width:100%;max-height:400px;object-fit:contain;" />`
              : `<div style="font-size:48px;margin-bottom:12px;">📐</div>
                 <h4 style="color:var(--navy,#0f172a);margin-bottom:6px;font-weight:700;">MIW Technical Engineering Diagram</h4>
                 <p style="color:var(--grey-text,#64748b);font-size:13px;max-width:480px;margin:0 auto 12px;">Original vector schematic in progress by the Maritime Intelligence Weekly graphics team. Framework linked to repository metadata.</p>
                 <span style="font-size:11px;background:var(--teal-light,#ccfbf1);color:var(--teal-dark,#0f766e);padding:4px 12px;border-radius:12px;font-weight:700;">Phase 2 Repository Linked</span>`
            }
          </div>
          <p style="font-size:14px;line-height:1.6;color:var(--ink,#0f172a);margin-bottom:20px;">${R.esc(ill.description)}</p>
          
          <div style="border-top:1px solid var(--grey-border,#e2e8f0);padding-top:16px;">
            <h4 style="font-size:12px;text-transform:uppercase;letter-spacing:1px;color:var(--teal-dark,#0f766e);margin-bottom:8px;">Linked Engineering Objects</h4>
            <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px;">
              ${(ill.engineeringObjectLinks || []).map(l => `<button type="button" class="xref ill-eo-link" data-id="${R.esc(l.targetId)}" style="padding:4px 10px;background:var(--grey-bg,#f1f5f9);border:1px solid var(--grey-border,#e2e8f0);border-radius:6px;font-size:12px;cursor:pointer;color:var(--teal-dark,#0f766e);font-weight:600;">⚙️ ${R.esc(l.targetId)}</button>`).join('') || '<span style="font-size:12px;color:var(--grey-text,#64748b);">None</span>'}
            </div>

            <h4 style="font-size:12px;text-transform:uppercase;letter-spacing:1px;color:var(--teal-dark,#0f766e);margin-bottom:8px;">Linked Regulations &amp; Standards</h4>
            <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px;">
              ${(ill.standardLinks || []).map(l => `<button type="button" class="xref ill-std-link" data-id="${R.esc(l.targetId)}" style="padding:4px 10px;background:var(--grey-bg,#f1f5f9);border:1px solid var(--grey-border,#e2e8f0);border-radius:6px;font-size:12px;cursor:pointer;color:var(--navy,#0f172a);font-weight:600;">📜 ${R.esc(l.targetId)}</button>`).join('') || '<span style="font-size:12px;color:var(--grey-text,#64748b);">None</span>'}
            </div>
            
            <div style="font-size:11px;color:var(--grey-text,#64748b);border-top:1px solid var(--grey-border,#e2e8f0);padding-top:12px;display:flex;justify-content:space-between;">
              <span>Copyright: ${R.esc(ill.copyright || 'Copyright © Maritime Intelligence Weekly')}</span>
              <span>Creator: ${R.esc(ill.creator || 'MIW Technical Team')}</span>
            </div>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    document.getElementById('close-ill-modal').addEventListener('click', () => modal.remove());
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });

    modal.querySelectorAll('.ill-eo-link').forEach(btn => btn.addEventListener('click', () => {
      modal.remove();
      window.RulesNav.showTab('engineering');
      if (window.RulesEngineering) window.RulesEngineering.init();
    }));

    modal.querySelectorAll('.ill-std-link').forEach(btn => btn.addEventListener('click', () => {
      modal.remove();
      window.RulesNav.showTab('search');
      R.showDetail(btn.dataset.id);
    }));
  }

  function renderGrid() {
    const grid = document.getElementById('illustration-grid');
    if (!grid) return;
    const items = DB.getIllustrations ? DB.getIllustrations() : [];
    if (!items || !items.length) {
      grid.innerHTML = `
        <div style="background:#fff;border:1px solid var(--grey-border,#e2e8f0);border-radius:12px;padding:32px;text-align:center;width:100%;">
          <div style="font-size:42px;margin-bottom:12px;">📐</div>
          <h3 style="color:var(--navy,#0f172a);font-weight:700;margin-bottom:8px;">Illustration Framework Active (Phase 2 UI Integrated)</h3>
          <p style="color:var(--grey-text,#64748b);font-size:14px;max-width:540px;margin:0 auto 16px;">The repository illustration schema, SVG viewer, and metadata loaders are fully integrated. Original vector schematics will be added as repository expansion packages evolve post-Version 1.0.</p>
          <span style="font-size:12px;background:var(--teal-light,#ccfbf1);color:var(--teal-dark,#0f766e);padding:5px 14px;border-radius:16px;font-weight:700;">Framework Ready · 0 Authoring Overhead</span>
        </div>
      `;
      return;
    }

    grid.innerHTML = items.map(ill => `
      <div class="eo-card ill-card" data-id="${R.esc(ill.id)}" style="cursor:pointer;">
        <div class="eo-card-title">📐 ${R.esc(ill.title)}</div>
        <div class="eo-card-kind">${R.esc(ill.illustrationType)}</div>
        <div class="eo-card-desc">${R.esc((ill.description || '').slice(0, 140))}${ill.description && ill.description.length > 140 ? '…' : ''}</div>
        <div class="eo-card-count">Linked to ${(ill.engineeringObjectLinks || []).length} Engineering Object(s)</div>
      </div>
    `).join('');

    grid.querySelectorAll('.ill-card').forEach(card => {
      card.addEventListener('click', () => {
        const ill = items.find(x => x.id === card.dataset.id);
        if (ill) openIllustrationModal(ill);
      });
    });
  }

  function init() {
    renderGrid();
  }

  return { init, openIllustrationModal };
})();
