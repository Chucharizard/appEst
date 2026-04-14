// ─── Datos de ejemplo del enunciado ───────────────────────────
const EXAMPLE_DATA = `12 13 9.5 10 8 10 9 8 8.5 9
10.1 9.2 8.1 8.2 8.1 8.3 8.1 9.2 9.4 10
10 9 8.5 12 8.1 8 8.3 9.3 14 14.5`;

function loadExample() {
  const ta = document.getElementById("datos");
  ta.value = EXAMPLE_DATA;
  ta.dispatchEvent(new Event("input"));
  ta.focus();
  // Animación de pulso en el textarea
  ta.classList.add("pulse");
  setTimeout(() => ta.classList.remove("pulse"), 600);
}

// ─── Submit con spinner ────────────────────────────────────────
const form = document.getElementById("statsForm");
const btn  = document.getElementById("submitBtn");

form?.addEventListener("submit", () => {
  btn.innerHTML = `<span class="spinner"></span> Calculando…`;
  btn.disabled = true;
});

// ─── Auto-scroll a resultados ─────────────────────────────────
window.addEventListener("DOMContentLoaded", () => {
  const first = document.querySelector(".result-section");
  if (first) {
    setTimeout(() => first.scrollIntoView({ behavior: "smooth", block: "start" }), 150);
  }
});

// ─── Notificación inline (reemplaza alert) ───────────────────
function showOcrNotification(msg, type) {
  const area = document.getElementById("ocrNotifArea");
  if (!area) return;
  const prev = area.querySelector(".ocr-notification");
  if (prev) prev.remove();
  const icon = type === "error" ? "⚠️" : "✓";
  const div = document.createElement("div");
  div.className = `ocr-notification ${type}`;
  div.innerHTML = `<span>${icon}</span><span>${msg}</span>`;
  area.appendChild(div);
  setTimeout(() => div.remove(), 5000);
}

// ─── Tesseract.js OCR Logic ───────────────────────────────────
const ocrCameraBtn = document.getElementById("ocrCameraBtn");
const ocrFileBtn = document.getElementById("ocrFileBtn");
const ocrCameraInput = document.getElementById("ocrCameraInput");
const ocrFileInput = document.getElementById("ocrFileInput");

const ocrOverlay = document.getElementById("ocrOverlay");
const ocrStatus = document.getElementById("ocrStatus");
const ta = document.getElementById("datos");

const handleOcrFile = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  // Mostrar overlay
  ocrOverlay.style.display = "flex";
  ocrStatus.innerText = "Iniciando motor Tesseract OCR (eng+spa)...";

  try {
    const { data: { text } } = await Tesseract.recognize(
      file,
      'eng+spa',
      {
        logger: m => {
          if (m.status === "recognizing text") {
            const p = Math.round(m.progress * 100);
            ocrStatus.innerText = `Reconociendo texto: ${p}%`;
          } else {
            ocrStatus.innerText = m.status;
          }
        }
      }
    );

    console.log("Raw OCR Text:", text);
    const regex = /\b\d+(?:[.,]\d+)?\b/g;
    const matches = text.match(regex);

    if (matches && matches.length > 0) {
      ta.value = matches.join(" ");
      ta.dispatchEvent(new Event("input"));
      ta.focus();
      ta.classList.add("pulse");
      setTimeout(() => ta.classList.remove("pulse"), 600);
      showOcrNotification(`Se extrajeron ${matches.length} valores de la imagen.`, "success");
    } else {
      showOcrNotification("No se encontraron números reconocibles en la imagen.", "error");
    }
  } catch (err) {
    console.error(err);
    showOcrNotification("Error al procesar la imagen con OCR.", "error");
  } finally {
    ocrOverlay.style.display = "none";
    e.target.value = ""; // reset
  }
};

if (ocrCameraBtn && ocrCameraInput) {
  ocrCameraBtn.addEventListener("click", () => ocrCameraInput.click());
  ocrCameraInput.addEventListener("change", handleOcrFile);
}

if (ocrFileBtn && ocrFileInput) {
  ocrFileBtn.addEventListener("click", () => ocrFileInput.click());
  ocrFileInput.addEventListener("change", handleOcrFile);
}

// ─── Lógica para UI Arbitraria ──────────────────────────────
window.toggleMetodo = function() {
  const method = document.querySelector('input[name="metodo"]:checked').value;
  document.getElementById('arbitrarioInput').style.display = method === 'arbitrario' ? 'flex' : 'none';
};


