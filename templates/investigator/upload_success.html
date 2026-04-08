{% extends "base.html" %}
{% block content %}

<style>
  .success-wrap{
    width:100%;
    background:
      radial-gradient(1100px 520px at -15% -20%, color-mix(in oklab, var(--brand) 22%, transparent), transparent 60%),
      radial-gradient(1100px 520px at 110% 120%, color-mix(in oklab, var(--blue) 18%, transparent), transparent 60%);
    border-radius:18px;
    padding:2rem 1.25rem 3rem;
  }

  /* Hero */
  .success-hero{
    position:relative;
    background:linear-gradient(135deg, var(--brand), var(--blue));
    color: var(--navy);
    border:1px solid var(--ring);
    border-radius:18px;
    box-shadow:0 20px 45px rgba(0,0,0,.28);
    padding:2.5rem 1.5rem;
    text-align:center;
    margin-bottom:2.5rem;
  }
  .success-hero h2{font-weight:900;font-size:2rem;margin:0 0 .35rem 0;color:#001a27;}
  .success-hero p{margin:0;color:#022232;font-weight:600;}
  .success-hero .check{font-size:3rem;margin-bottom:.35rem;}

  /* Receipt card – wider and roomier */
  .receipt-card{
    background:var(--card);
    color:var(--text);
    border:1px solid var(--ring);
    border-radius:20px;
    box-shadow:0 12px 36px rgba(0,0,0,.35);
    max-width:1100px;
    margin:0 auto;
    padding:2.25rem 2rem;
  }

  .meta-grid{
    display:grid;
    grid-template-columns:1fr;
    gap:1.5rem;
  }
  @media(min-width:900px){
    .meta-grid{ grid-template-columns:1.2fr 1fr; gap:2rem; align-items:start; }
  }

  .file-box, .hash-box{
    background: color-mix(in oklab, var(--card) 92%, black 8%);
    border:1px solid color-mix(in oklab, var(--ring) 70%, transparent);
    border-radius:16px;
    padding:1.5rem 1.4rem;
  }

  .file-box h3{margin:.25rem 0 .4rem; font-size:1.35rem;}
  .muted{color:var(--muted); font-size:.95rem;}
  .hash-row{display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:.6rem;}

  .tag{
    display:inline-flex; align-items:center; gap:.35rem;
    background: color-mix(in oklab, var(--bg) 80%, var(--blue) 20%);
    color: var(--text);
    border:1px solid var(--ring);
    padding:.35rem .7rem;
    border-radius:999px;
    font-size:.85rem; font-weight:700;
  }

  .mono{
    display:block;
    width:100%;
    background: color-mix(in oklab, var(--bg) 85%, black 15%);
    border:1px solid color-mix(in oklab, var(--ring) 70%, transparent);
    border-radius:10px;
    padding:1rem 1.25rem;
    font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size:.95rem;
    color:var(--text);
    word-wrap:break-word;
  }

  .actions{
    display:flex;
    flex-wrap:wrap;
    gap:.8rem;
    margin-top:1.25rem;
  }
  .btn-soft{
    background: color-mix(in oklab, var(--bg) 78%, var(--brand) 22%);
    color: var(--text);
    border:1px solid var(--ring);
    padding:.75rem 1.25rem;
    border-radius:10px;
    font-weight:800;
    cursor:pointer;
    transition:transform .2s ease, background .2s ease;
  }
  .btn-soft:hover{
    transform:translateY(-1px);
    background: color-mix(in oklab, var(--bg) 70%, var(--brand) 30%);
  }

  .footer-actions{
    display:flex;
    flex-wrap:wrap;
    gap:1rem;
    justify-content:center;
    margin-top:2rem;
  }
  .btn-link{
    text-decoration:none;
    display:inline-flex;
    align-items:center;
    gap:.6rem;
    font-weight:800;
    border-radius:12px;
    padding:.9rem 1.4rem;
  }
  .btn-outline{ color:var(--text); background:transparent; border:1px solid var(--ring);}
  .btn-primary{ background:var(--brand); color:#001220;}
  .btn-success{ background:var(--yellow); color: var(--navy);}
  .tip{margin-top:1rem; color:var(--muted); font-size:.95rem; line-height:1.6;}

  .confetti{position:absolute; inset:0; pointer-events:none;}
  .confetti i{
    position:absolute;width:8px;height:14px;opacity:.9;border-radius:2px;
    animation:fall 900ms ease-out forwards;
  }
  @keyframes fall{
    0%{transform:translateY(-24px) rotate(0deg);}
    100%{transform:translateY(120px) rotate(360deg);opacity:0;}
  }
</style>

<div class="success-wrap">
  <div class="success-hero">
    <div class="check">✅</div>
    <h2>Evidence Uploaded Successfully</h2>
    <p>Your file is encrypted, hashed, and recorded on the blockchain.</p>
    <div class="confetti" id="confetti"></div>
  </div>

  <div class="receipt-card"
       id="receipt"
       data-filename="{{ filename }}"
       data-hash="{{ file_hash }}"
       data-block="{{ block_id }}"
       data-when="{{ now().strftime('%Y-%m-%d %H:%M:%S') if now else '' }}">
    <div class="meta-grid">

      <!-- Left column -->
      <div class="file-box">
        <span class="tag">📁 File</span>
        <h3>{{ filename }}</h3>
        <div class="muted">Stored in the secure evidence vault.</div>

        <div style="margin-top:1.2rem;">
          <span class="tag">⛓️ Block ID</span>
          <div class="mono" style="margin-top:.5rem;">#{{ block_id }}</div>
        </div>

        <div style="margin-top:1.2rem;">
          <span class="tag">🕒 Timestamp</span>
          <div class="mono" style="margin-top:.5rem;">
            {{ now().strftime("%d %b %Y, %H:%M") if now else '' }}
          </div>
        </div>
      </div>

      <!-- Right column -->
      <div class="hash-box">
        <div class="hash-row">
          <span class="tag">🔐 SHA-256 Hash</span>
          <button class="btn-soft" id="copyHash" type="button">📋 Copy hash</button>
        </div>
        <pre class="mono" id="hashText" style="margin-top:.7rem;">{{ file_hash }}</pre>

        <div class="actions">
          <button class="btn-soft" type="button" id="downloadJSON">⬇️ Download receipt (.json)</button>
          <button class="btn-soft" type="button" onclick="window.print()">🖨️ Print receipt</button>
        </div>

        <div class="tip">
          Keep this receipt — re-hashing the same file later should yield the same SHA-256 if it’s untampered.
        </div>
      </div>
    </div>

    <!-- Footer buttons -->
    <div class="footer-actions">
      <a href="{{ url_for('investigator_bp.upload_evidence') }}" class="btn-link btn-outline">⬆️ Upload Another</a>
      <a href="{{ url_for('investigator_bp.view_ledger') }}" class="btn-link btn-success">🔗 View Blockchain Ledger</a>
      <a href="{{ url_for('investigator_bp.dashboard') }}" class="btn-link btn-primary">🏠 Back to Dashboard</a>
    </div>
  </div>
</div>

<script>
  // Copy hash
  document.getElementById('copyHash')?.addEventListener('click', async () => {
    const text = document.getElementById('hashText').innerText.trim();
    try {
      await navigator.clipboard.writeText(text);
      const btn = document.getElementById('copyHash');
      const old = btn.textContent;
      btn.textContent = '✅ Copied';
      setTimeout(()=> btn.textContent = old, 1200);
    } catch {
      alert('Copy failed. Please copy manually.');
    }
  });

  // Download JSON receipt
  document.getElementById('downloadJSON')?.addEventListener('click', () => {
    const r = document.getElementById('receipt');
    const payload = {
      filename: r.dataset.filename || "{{ filename }}",
      sha256: r.dataset.hash || "{{ file_hash }}",
      block_id: r.dataset.block || "{{ block_id }}",
      timestamp: r.dataset.when || "{{ now().strftime('%Y-%m-%d %H:%M:%S') if now else '' }}"
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const safe = (payload.filename || 'evidence').replace(/[^\w.-]+/g,'_');
    a.href = url; a.download = `${safe}_receipt.json`;
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
  });

  // Confetti
  (function confetti(){
    const host = document.getElementById('confetti');
    if(!host) return;
    const colors = [getCSS('--yellow'), getCSS('--brand'), getCSS('--blue'), getCSS('--accent')].filter(Boolean);
    for(let i=0;i<28;i++){
      const s=document.createElement('i');
      s.style.left=(8+Math.random()*84)+'%';
      s.style.top=(-10+Math.random()*10)+'px';
      s.style.background=colors[Math.floor(Math.random()*colors.length)];
      s.style.transform=`rotate(${Math.random()*180}deg)`;
      host.appendChild(s);
      setTimeout(()=>s.remove(),1100);
    }
    function getCSS(v){return getComputedStyle(document.documentElement).getPropertyValue(v)?.trim();}
  })();
</script>

{% endblock %}
