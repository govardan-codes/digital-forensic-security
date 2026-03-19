{% extends "base.html" %}
{% block content %}

<style>
  /* ===== Verify Evidence Page ===== */
  .verify-wrapper{
    width:100%;
    background:
      radial-gradient(1000px 520px at -15% -20%, color-mix(in oklab, var(--brand) 25%, transparent), transparent 60%),
      radial-gradient(1000px 520px at 110% 120%, color-mix(in oklab, var(--blue) 20%, transparent), transparent 60%);
    border-radius:18px;
    padding:2rem 1rem 3rem;
  }

  /* Hero section */
  .verify-hero{
    background:linear-gradient(135deg, var(--brand), var(--blue));
    color:var(--navy);
    border-radius:18px;
    padding:2rem 1.5rem;
    text-align:center;
    margin-bottom:2.5rem;
    box-shadow:0 12px 30px rgba(0,0,0,.3);
  }
  .verify-hero h2{font-weight:900;font-size:2rem;margin-bottom:.5rem;}
  .verify-hero p{color:#022232;max-width:900px;margin:0 auto;font-size:1.05rem;}

  /* Upload section */
  .verify-card{
    background:var(--card);
    border:1px solid var(--ring);
    border-radius:18px;
    box-shadow:0 10px 30px rgba(0,0,0,.25);
    max-width:700px;
    margin:0 auto;
    padding:2rem 1.75rem;
  }

  .drop-zone{
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    border:2px dashed var(--blue);
    border-radius:14px;
    padding:2.5rem 1rem;
    cursor:pointer;
    transition:all .3s ease;
    color:var(--muted);
    text-align:center;
  }
  .drop-zone:hover{
    border-color:var(--yellow);
    background:rgba(255,193,7,.06);
  }
  .drop-zone.dragover{
    border-color:var(--brand);
    background:rgba(58,208,255,.08);
  }

  .file-name{
    color:var(--blue);
    font-weight:700;
    margin-top:1rem;
    word-break:break-all;
  }

  /* Button */
  .btn-verify{
    background:var(--yellow);
    color:var(--navy);
    border:none;
    border-radius:40px;
    padding:0.9rem 2.5rem;
    font-weight:800;
    font-size:1rem;
    cursor:pointer;
    box-shadow:0 6px 18px rgba(0,0,0,.18);
    transition:transform .25s ease, background .25s ease;
    margin-top:1.5rem;
  }
  .btn-verify:hover{
    background:var(--bright-yellow);
    transform:translateY(-2px);
  }

  /* Progress bar */
  .progress-wrap{
    display:none;
    width:100%;
    height:10px;
    margin-top:1.5rem;
    background:rgba(255,255,255,.1);
    border-radius:999px;
    overflow:hidden;
  }
  .progress-inner{
    height:100%;
    width:0%;
    background:linear-gradient(90deg, var(--brand), var(--yellow));
    transition:width .3s ease;
  }

  /* Info note */
  .info-note{
    max-width:850px;
    margin:2.5rem auto 0;
    background:rgba(0,0,139,.05);
    border-left:5px solid var(--yellow);
    border-radius:12px;
    padding:1.25rem 1.5rem;
    color:var(--text);
    font-size:1rem;
    line-height:1.7;
  }
  .info-note strong{color:var(--blue);}

  @media(max-width:700px){
    .verify-card{padding:1.5rem 1rem;}
    .drop-zone{padding:2rem .75rem;}
  }
</style>

<div class="verify-wrapper">
  <!-- Hero -->
  <div class="verify-hero">
    <h2>🧩 Verify Digital Evidence</h2>
    <p>
      Upload a previously submitted file to check its authenticity
      against the blockchain record.
    </p>
  </div>

  <!-- Form -->
  <div class="verify-card">
    <form action="{{ url_for('investigator_bp.verify_evidence') }}" method="POST" enctype="multipart/form-data" onsubmit="showProgressBar()">
      <div id="dropZone" class="drop-zone" role="button" tabindex="0">
        <div style="font-size:1.8rem;margin-bottom:.25rem;">📁</div>
        <div><strong>Click to choose a file</strong> or drag & drop it here</div>
        <small style="color:#999;margin-top:.35rem;">Supported: images, PDFs, text, archives</small>
      </div>
      <input type="file" id="verify_file" name="verify_file" required style="display:none;" onchange="previewFileName(event)">
      <p id="file-name" class="file-name"></p>

      <div style="text-align:center;">
        <button type="submit" class="btn-verify">🔍 Verify Authenticity</button>
      </div>

      <!-- Progress -->
      <div class="progress-wrap" id="progressWrap">
        <div class="progress-inner" id="progressInner"></div>
      </div>
    </form>
  </div>

  <!-- Note -->
  <div class="info-note">
    💡 <strong>Note:</strong> The system computes a <strong>SHA-256 hash</strong> of your uploaded file and compares it with
    the original blockchain record. If they differ, the file may have been <strong>modified</strong> or <strong>corrupted</strong>.
  </div>
</div>

<!-- Script -->
<script>
  const fileInput = document.getElementById('verify_file');
  const dropZone  = document.getElementById('dropZone');
  const fileName  = document.getElementById('file-name');

  // File name preview
  function previewFileName(event){
    const file = event.target.files[0];
    fileName.textContent = file ? `📄 ${file.name}` : '';
  }

  // Click / keyboard open
  dropZone.addEventListener('click', () => fileInput.click());
  dropZone.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      fileInput.click();
    }
  });

  // Drag & drop
  ['dragenter','dragover'].forEach(evt => 
    dropZone.addEventListener(evt, e => {
      e.preventDefault(); e.stopPropagation();
      dropZone.classList.add('dragover');
    })
  );
  ['dragleave','drop'].forEach(evt => 
    dropZone.addEventListener(evt, e => {
      e.preventDefault(); e.stopPropagation();
      dropZone.classList.remove('dragover');
    })
  );
  dropZone.addEventListener('drop', e => {
    const files = e.dataTransfer.files;
    if (files && files.length) {
      fileInput.files = files;
      previewFileName({ target: fileInput });
    }
  });

  // Progress bar animation
  function showProgressBar(){
    const bar = document.getElementById('progressWrap');
    const inner = document.getElementById('progressInner');
    if(!bar || !inner) return;
    bar.style.display = 'block';
    inner.style.width = '0%';
    let w = 0;
    const t = setInterval(()=>{
      w += 10;
      inner.style.width = Math.min(w,100) + '%';
      if(w >= 100) clearInterval(t);
    },120);
  }
</script>

{% endblock %}
