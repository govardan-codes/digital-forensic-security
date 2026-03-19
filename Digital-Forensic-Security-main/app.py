{% extends "base.html" %}
{% block content %}

<style>
  .upload-wrapper{
    width:100%;
    background:
      radial-gradient(1100px 520px at -10% -10%, rgba(255,193,7,.10), transparent 60%),
      radial-gradient(1100px 520px at 110% 110%, rgba(0,0,139,.06), transparent 60%);
    border-radius:18px;
    padding:3rem 1.5rem 4rem;
  }
  .upload-header{ text-align:center; margin-bottom:2.25rem; }
  .upload-header h2{ color:var(--blue); font-weight:900; font-size:2rem; margin:.25rem 0; }
  .upload-header p{ color:var(--muted); font-size:1.05rem; max-width:720px; margin:0 auto; }

  .upload-card{
    background:#fff; border-radius:20px; box-shadow:0 10px 35px rgba(0,0,0,.08);
    max-width:650px; margin:0 auto; padding:2.25rem 1.75rem; text-align:center;
  }

  /* Full-width, non-overflow drop zone */
  .upload-box{
    display:flex; width:100%; box-sizing:border-box; min-height:150px;
    border:2px dashed #1a237e; border-radius:14px; padding:2rem 1rem;
    cursor:pointer; transition:all .2s ease; color:#444; font-size:1.05rem;
    align-items:center; justify-content:center; flex-direction:column; background:#fff;
  }
  .upload-box:hover{ border-color:var(--yellow); background:rgba(255,193,7,.06); }
  .upload-box:focus{ outline:3px solid rgba(255,193,7,.25); outline-offset:4px; }
  .upload-box.dragover{ outline:4px solid rgba(255,193,7,.45); outline-offset:5px; }

  #file-name{ color:var(--blue); font-weight:700; margin-top:1rem; word-break:break-all; }

  .btn-upload{
    background:linear-gradient(135deg, var(--yellow), #ffb400);
    color:var(--navy); border:none; border-radius:40px;
    padding:.9rem 2.5rem; font-weight:800; font-size:1rem; cursor:pointer;
    box-shadow:0 6px 18px rgba(0,0,0,.18);
    transition:transform .25s ease, background .25s ease;
    margin-top:1.6rem;
  }
  .btn-upload:hover{ background:var(--bright-yellow); transform:translateY(-2px); }

  .info-note{
    max-width:850px; margin:2.2rem auto 0;
    background:rgba(0,0,139,.05);
    border-left:5px solid var(--yellow); border-radius:12px;
    padding:1.1rem 1.3rem; color:var(--navy); font-size:1rem; line-height:1.7;
  }
  .info-note strong{ color:var(--blue); }

  @media (max-width:800px){
    .upload-card{ padding:1.75rem 1.1rem; }
    .upload-box{ padding:1.6rem .75rem; min-height:130px; }
  }
</style>

<div class="upload-wrapper">
  <div class="upload-header">
    <h2>📤 Upload Digital Evidence</h2>
    <p>
      Select a file to upload. It will be automatically <strong>encrypted</strong>, <strong>hashed</strong>,
      and securely recorded in the <strong>blockchain ledger</strong>.
    </p>
  </div>

  <div class="upload-card">
    <form action="{{ url_for('investigator_bp.upload_evidence') }}" method="POST" enctype="multipart/form-data">
      <!-- Div acts like a button: no 'for' binding => no double dialog -->
      <div
        id="dropZone"
        class="upload-box"
        role="button"
        tabindex="0"
        aria-controls="evidence_file"
        aria-label="Choose a file or drag and drop"
      >
        <div style="font-size:1.8rem; margin-bottom:.25rem;">📁</div>
        <div><strong>Click to choose a file</strong> or drag & drop it here</div>
        <small style="color:#555; margin-top:.35rem;">Supported: images, PDFs, text, and archives</small>
      </div>

      <input
        type="file"
        id="evidence_file"
        name="evidence_file"
        required
        style="display:none;"
        onchange="previewFileName(event)"
      >
      <p id="file-name"></p>

      <button type="submit" class="btn-upload">🔒 Upload & Secure</button>
    </form>
  </div>

  <div class="info-note">
    💡 <strong>Note:</strong> Once uploaded, your file’s unique <strong>SHA-256 hash</strong> and encryption key
    will be permanently recorded on the blockchain for future authenticity verification.
  </div>
</div>

<script>
  const fileInput = document.getElementById('evidence_file');
  const dropZone  = document.getElementById('dropZone');
  const fileName  = document.getElementById('file-name');

  function previewFileName(e){
    const f = e.target.files[0];
    fileName.textContent = f ? `📄 ${f.name}` : '';
  }

  // Click / keyboard open (single dialog)
  dropZone.addEventListener('click', () => fileInput.click());
  dropZone.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      fileInput.click();
    }
  });

  // Drag & drop
  ['dragenter','dragover'].forEach(evt =>
    dropZone.addEventListener(evt, (e) => {
      e.preventDefault(); e.stopPropagation();
      dropZone.classList.add('dragover');
    })
  );
  ['dragleave','drop'].forEach(evt =>
    dropZone.addEventListener(evt, (e) => {
      e.preventDefault(); e.stopPropagation();
      dropZone.classList.remove('dragover');
    })
  );
  dropZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files && files.length) {
      fileInput.files = files;
      previewFileName({ target: fileInput });
    }
  });
</script>

{% endblock %}
