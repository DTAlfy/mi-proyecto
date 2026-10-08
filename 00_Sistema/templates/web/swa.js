/* =============================================================================
   SpanishWithAlfy · Componentes de los materiales web (vanilla JS, sin dependencias)
   Cada página lleva sus datos en <script type="application/json" id="swa-datos">
   y un contenedor [data-componente="..."]. Este archivo pinta el componente.
   ============================================================================= */
(() => {
  "use strict";

  // ------------------------------------------------------------ utilidades
  const h = (tag, attrs = {}, ...hijos) => {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === false || v == null) continue;
      if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
      else if (k === "html") el.innerHTML = v;
      else el.setAttribute(k, v === true ? "" : v);
    }
    for (const hijo of hijos.flat()) if (hijo != null && hijo !== false) el.append(hijo.nodeType ? hijo : String(hijo));
    return el;
  };
  const almacen = {
    leer(clave, defecto) {
      try { const v = localStorage.getItem(clave); return v ? JSON.parse(v) : defecto; } catch { return defecto; }
    },
    guardar(clave, valor) { try { localStorage.setItem(clave, JSON.stringify(valor)); } catch { /* modo privado */ } },
    borrar(clave) { try { localStorage.removeItem(clave); } catch { /* nada */ } },
  };
  const dinero = (n, moneda = "$") => moneda + Math.round(n).toLocaleString("es");
  const avisar = (texto) => {
    let t = document.querySelector(".toast");
    if (!t) { t = h("div", { class: "toast", role: "status", "aria-live": "polite" }); document.body.append(t); }
    t.textContent = texto; t.classList.add("visible");
    clearTimeout(t._timer); t._timer = setTimeout(() => t.classList.remove("visible"), 1800);
  };
  const copiar = async (texto) => {
    try { await navigator.clipboard.writeText(texto); avisar("Copiado ✓"); } catch { avisar("No se pudo copiar"); }
  };
  const ICONO_PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.5-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg>';

  const panel = (titulo, sub, ...hijos) => h("section", { class: "panel" },
    titulo && h("h2", {}, titulo), sub && h("p", { class: "sub" }, sub), ...hijos);

  // ------------------------------------------------------------ 1. calculadora
  function calculadora(raiz, d, id) {
    const clave = `swa:${id}`;
    const v = Object.assign({}, d.valores, almacen.leer(clave, {}));
    const campos = [
      { k: "precio", nombre: "Precio por hora", min: 5, max: 60, paso: 1, fmt: (x) => dinero(x, d.moneda) },
      { k: "comision", nombre: "Comisión de la plataforma", min: 0, max: 40, paso: 1, fmt: (x) => `${x}%`, ayuda: d.nota_comision },
      { k: "impuestos", nombre: "Impuestos estimados", min: 0, max: 40, paso: 1, fmt: (x) => `${x}%` },
      { k: "horas", nombre: "Horas de clase por semana", min: 1, max: 40, paso: 1, fmt: (x) => `${x} h` },
    ];
    const salidas = {};
    const controles = campos.map((c) => {
      const out = h("output", {}, c.fmt(v[c.k]));
      const rango = h("input", { type: "range", min: c.min, max: c.max, step: c.paso, value: v[c.k], "aria-label": c.nombre,
        oninput: (e) => { v[c.k] = Number(e.target.value); out.textContent = c.fmt(v[c.k]); calcular(); } });
      return h("div", { class: "campo" }, h("div", { class: "deslizador" }, h("span", { class: "etiqueta" }, c.nombre), out, rango),
        c.ayuda && h("span", { class: "ayuda" }, c.ayuda));
    });
    for (const k of ["bruto", "neto", "netoHora"]) salidas[k] = h("div", { class: "valor" }, "–");
    const barra = h("i"); const metaTxt = h("span"); const faltan = h("span");
    const cuerpo = h("tbody");
    raiz.append(
      h("div", { class: "grid dos" },
        panel("Tus números", "Mueve los controles: el cálculo es instantáneo y se guarda en este navegador.", h("div", { class: "grid" }, controles)),
        panel("Tu resultado mensual", `Meta del curso: ${dinero(d.meta_mensual, d.moneda)} netos al mes.`,
          h("div", { class: "grid tres" },
            h("div", { class: "kpi" }, h("div", { class: "nombre" }, "Bruto al mes"), salidas.bruto),
            h("div", { class: "kpi destacado" }, h("div", { class: "nombre" }, "Neto al mes"), salidas.neto),
            h("div", { class: "kpi" }, h("div", { class: "nombre" }, "Neto por hora"), salidas.netoHora)),
          h("div", { class: "meta-texto" }, metaTxt, faltan),
          h("div", { class: "barra", role: "progressbar", "aria-label": "Progreso hacia la meta" }, barra))),
      panel("Tu escalera de precios", "Horas semanales necesarias para la meta en cada escalón, con tu comisión e impuestos.",
        h("div", { class: "scroll-x" }, h("table", { class: "tabla" },
          h("thead", {}, h("tr", {}, h("th", {}, "Precio/hora"), h("th", {}, "Neto por hora"), h("th", {}, "Horas/semana para la meta"))),
          cuerpo))),
      h("p", { class: "nota" }, "ⓘ ", d.nota));

    function calcular() {
      const factor = (1 - v.comision / 100) * (1 - v.impuestos / 100);
      const bruto = v.precio * v.horas * d.semanas_por_mes;
      const neto = bruto * factor;
      salidas.bruto.textContent = dinero(bruto, d.moneda);
      salidas.neto.textContent = dinero(neto, d.moneda);
      salidas.netoHora.textContent = dinero(v.precio * factor, d.moneda);
      const pct = Math.min(100, (neto / d.meta_mensual) * 100);
      barra.style.width = `${pct}%`;
      metaTxt.textContent = `${Math.round(pct)}% de la meta`;
      const horasMeta = d.meta_mensual / (v.precio * factor * d.semanas_por_mes);
      faltan.textContent = neto >= d.meta_mensual ? "¡Meta alcanzada!" : `Necesitas ≈ ${Math.ceil(horasMeta)} h/semana a este precio`;
      cuerpo.replaceChildren(...d.escalones.map((p) => {
        const n = p * factor;
        return h("tr", { class: Math.abs(p - v.precio) < 2.5 ? "activa" : "" },
          h("td", {}, dinero(p, d.moneda)), h("td", {}, dinero(n, d.moneda)),
          h("td", {}, `${Math.ceil(d.meta_mensual / (n * d.semanas_por_mes))} h`));
      }));
      almacen.guardar(clave, v);
    }
    calcular();
  }

  // ------------------------------------------------------------ 2. diagnóstico
  function diagnostico(raiz, d, id) {
    const clave = `swa:${id}`;
    const estado = almacen.leer(clave, { valores: {}, historial: [] });
    const valores = Object.assign({}, Object.fromEntries(d.campos.map((c) => [c.id, c.tipo === "sino" ? "no" : 0])), estado.valores);
    const entradas = d.campos.map((c) => {
      if (c.tipo === "sino") {
        const opcion = (val, txt) => h("label", {}, h("input", { type: "radio", name: c.id, value: val, checked: valores[c.id] === val,
          onchange: () => { valores[c.id] = val; actualizar(); } }), h("span", {}, txt));
        return h("div", { class: "campo" }, h("span", { class: "etiqueta" }, c.etiqueta),
          h("div", { class: "sino", role: "radiogroup", "aria-label": c.etiqueta }, opcion("si", "Sí"), opcion("no", "No")));
      }
      const idCampo = `${id}-${c.id}`;
      return h("div", { class: "campo" }, h("label", { for: idCampo }, c.etiqueta),
        h("input", { id: idCampo, type: "number", min: 0, step: c.paso || 1, value: valores[c.id], inputmode: "decimal",
          oninput: (e) => { valores[c.id] = Number(e.target.value) || 0; actualizar(); } }),
        c.ayuda && h("span", { class: "ayuda" }, c.ayuda));
    });
    const etapaEl = h("div", { class: "valor" }); const nombreEl = h("h3", {}); const prioridadEl = h("p", { class: "lead" });
    const leccionEl = h("span", { class: "chip" }); const ingresoEl = h("div", { class: "valor" }); const barra = h("i");
    const historialEl = h("tbody");
    const operar = { "==": (a, b) => a === b, "<": (a, b) => a < b, "<=": (a, b) => a <= b, ">": (a, b) => a > b, ">=": (a, b) => a >= b };
    const evaluar = () => d.reglas.find((r) => (r.si || []).every((c) => operar[c.op](valores[c.campo], c.valor))) || d.reglas[d.reglas.length - 1];

    raiz.append(
      h("div", { class: "grid dos" },
        panel("Tus cinco números de hoy", "Sé honesto: el punto de partida no se juzga, se mide.",
          h("div", { class: "grid" }, entradas),
          h("div", { class: "fila-botones" },
            h("button", { class: "btn", type: "button", onclick: guardarMedicion }, "Guardar medición"),
            h("button", { class: "btn fantasma", type: "button", onclick: borrarTodo }, "Borrar historial"))),
        panel("Tu etapa en el Roadmap", null,
          h("div", { class: "kpi destacado" }, h("div", { class: "nombre" }, "Etapa recomendada"), etapaEl),
          h("div", { style: "margin-top:18px;display:grid;gap:10px" }, nombreEl, prioridadEl, leccionEl),
          h("div", { class: "kpi", style: "margin-top:18px" }, h("div", { class: "nombre" }, "Ingreso bruto estimado al mes"), ingresoEl),
          h("div", { class: "barra", style: "margin-top:10px" }, barra))),
      panel("Tu evolución", "Cada medición guardada queda aquí. Mídete cada lunes: dos minutos.",
        h("div", { class: "scroll-x" }, h("table", { class: "tabla" },
          h("thead", {}, h("tr", {}, h("th", {}, "Fecha"), ...d.campos.filter((c) => c.tipo !== "sino").map((c) => h("th", {}, c.corto || c.etiqueta)), h("th", {}, "Etapa"))),
          historialEl))));

    function actualizar() {
      const r = evaluar();
      etapaEl.textContent = r.etapa; nombreEl.textContent = r.nombre; prioridadEl.textContent = r.prioridad;
      leccionEl.textContent = `Lección recomendada: ${r.leccion}`;
      const ingreso = (valores.precio || 0) * (valores.horas || 0) * d.semanas_por_mes;
      ingresoEl.textContent = dinero(ingreso, d.moneda);
      barra.style.width = `${Math.min(100, (ingreso / d.meta_mensual) * 100)}%`;
      almacen.guardar(clave, { valores, historial: estado.historial });
    }
    function pintarHistorial() {
      historialEl.replaceChildren(...(estado.historial.length ? estado.historial.slice().reverse().map((m) =>
        h("tr", {}, h("td", {}, m.fecha), ...d.campos.filter((c) => c.tipo !== "sino").map((c) => h("td", {}, m.valores[c.id] ?? "–")), h("td", {}, m.etapa)))
        : [h("tr", {}, h("td", { colspan: 10, style: "color:var(--muted)" }, "Aún no hay mediciones guardadas."))]));
    }
    function guardarMedicion() {
      estado.historial.push({ fecha: new Date().toLocaleDateString("es"), valores: { ...valores }, etapa: evaluar().etapa });
      almacen.guardar(clave, { valores, historial: estado.historial }); pintarHistorial(); avisar("Medición guardada ✓");
    }
    function borrarTodo() {
      if (!confirm("¿Borrar todas las mediciones guardadas en este navegador?")) return;
      estado.historial = []; almacen.guardar(clave, { valores, historial: [] }); pintarHistorial();
    }
    actualizar(); pintarHistorial();
  }

  // ------------------------------------------------------------ 3. hitos
  function hitos(raiz, d, id) {
    const clave = `swa:${id}`;
    const hechos = new Set(almacen.leer(clave, []));
    const total = d.etapas.reduce((n, e) => n + e.items.length, 0);
    const barraTotal = h("i"); const txtTotal = h("span");
    const tarjetas = d.etapas.map((e, i) => {
      const contador = h("span", { class: "hito" });
      const tarjeta = h("article", { class: "panel etapa" });
      const lista = e.items.map((item, j) => {
        const k = `e${i}-${j}`;
        return h("label", { class: "check" }, h("input", { type: "checkbox", checked: hechos.has(k),
          onchange: (ev) => { ev.target.checked ? hechos.add(k) : hechos.delete(k); actualizar(); } }), h("span", {}, item));
      });
      tarjeta.append(h("header", {}, h("div", { class: "num" }, i + 1),
        h("div", {}, h("h3", {}, e.titulo), h("div", { class: "hito" }, `Hito: ${e.hito}`), contador)), ...lista);
      tarjeta._actualizar = () => {
        const n = e.items.filter((_, j) => hechos.has(`e${i}-${j}`)).length;
        contador.textContent = `${n}/${e.items.length} completados`;
        tarjeta.classList.toggle("completa", n === e.items.length);
      };
      return tarjeta;
    });
    raiz.append(
      panel("Tu progreso total", "Marca cada acción cuando la completes. Se guarda en este navegador.",
        h("div", { class: "meta-texto" }, txtTotal, h("span", {}, `${total} acciones en ${d.etapas.length} etapas`)),
        h("div", { class: "barra" }, barraTotal),
        h("div", { class: "fila-botones" }, h("button", { class: "btn fantasma mini", type: "button",
          onclick: () => { if (confirm("¿Desmarcar todo?")) { hechos.clear(); raiz.querySelectorAll("input").forEach((x) => (x.checked = false)); actualizar(); } } }, "Reiniciar"))),
      h("div", { class: "grid dos", style: "margin-top:20px" }, tarjetas));
    function actualizar() {
      tarjetas.forEach((t) => t._actualizar());
      const pct = Math.round((hechos.size / total) * 100);
      barraTotal.style.width = `${pct}%`; txtTotal.textContent = `${pct}% del Roadmap completado`;
      almacen.guardar(clave, [...hechos]);
    }
    actualizar();
  }

  // ------------------------------------------------------------ 4. titular
  function titular(raiz, d, id) {
    const clave = `swa:${id}`;
    const v = Object.assign(Object.fromEntries(d.campos.map((c) => [c.id, ""])), almacen.leer(clave, {}));
    const salida = h("div", { class: "grid" });
    const inputs = {};
    const campos = d.campos.map((c) => {
      const idCampo = `${id}-${c.id}`;
      inputs[c.id] = h("input", { id: idCampo, type: "text", value: v[c.id], placeholder: c.ejemplo || "",
        oninput: (e) => { v[c.id] = e.target.value; pintar(); } });
      return h("div", { class: "campo" }, h("label", { for: idCampo }, c.etiqueta), inputs[c.id], c.ayuda && h("span", { class: "ayuda" }, c.ayuda));
    });
    const rellenar = (plantilla, conHuecos) => plantilla.replace(/\{(\w+)\}/g, (_, k) => {
      const valor = (v[k] || "").trim();
      if (valor) return conHuecos ? `<b>${valor.replace(/[&<>"]/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[m]))}</b>` : valor;
      const campo = d.campos.find((c) => c.id === k);
      return conHuecos ? `<span class="hueco">${campo && campo.opcional ? "" : `[${campo ? campo.etiqueta.toLowerCase() : k}]`}</span>` : "";
    }).replace(/\s+([,.:])/g, "$1").replace(/\s{2,}/g, " ").trim();
    function pintar() {
      salida.replaceChildren(...d.plantillas.map((p) => {
        const plano = rellenar(p.texto, false);
        return h("div", { class: "propuesta" },
          h("span", { class: "chip", style: "width:fit-content" }, p.idioma === "en" ? "English" : "Español"),
          h("div", { class: "texto", html: rellenar(p.texto, true) }),
          h("footer", {}, h("span", {}, `${plano.length} caracteres`),
            h("button", { class: "btn mini", type: "button", onclick: () => copiar(plano) }, "Copiar")));
      }));
      almacen.guardar(clave, v);
    }
    raiz.append(h("div", { class: "grid dos" },
      panel("Las tres piezas", "Para quién, qué resultado y qué te hace diferente.", h("div", { class: "grid" }, campos),
        h("div", { class: "fila-botones" }, h("button", { class: "btn fantasma", type: "button", onclick: () => {
          d.campos.forEach((c) => { v[c.id] = c.ejemplo || ""; inputs[c.id].value = v[c.id]; }); pintar(); } }, "Cargar ejemplo"))),
      panel("Tus titulares", "Elige el que no podría copiar ningún otro tutor.", salida)),
      h("p", { class: "nota" }, "ⓘ ", d.nota));
    pintar();
  }

  // ------------------------------------------------------------ 5. cronómetro
  function cronometro(raiz, d) {
    const fases = d.fases;
    let idx = 0, restante = fases[0].minutos * 60, corriendo = false, ultimo = 0, raf = 0;
    const R = 120, C = 2 * Math.PI * R;
    const progreso = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    progreso.setAttribute("class", "progreso"); progreso.setAttribute("cx", 130); progreso.setAttribute("cy", 130); progreso.setAttribute("r", R);
    progreso.style.strokeDasharray = C;
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg"); svg.setAttribute("viewBox", "0 0 260 260");
    svg.innerHTML = `<circle class="fondo" cx="130" cy="130" r="${R}"></circle>`; svg.append(progreso);
    const tiempoEl = h("div", { class: "tiempo", "aria-live": "off" }); const faseEl = h("div", { class: "fase" });
    const tituloEl = h("h3", { style: "font-size:1.6rem" }); const detalleEl = h("p", { class: "sub", style: "margin:6px 0 0" });
    const frasesEl = h("ul", { class: "frases" });
    const tramos = h("div", { class: "tramos" }, fases.map((f) => h("div", { style: `flex:${f.minutos}`, title: `${f.nombre} · ${f.minutos} min` })));
    const btnPlay = h("button", { class: "btn", type: "button", onclick: alternar }, "Iniciar");
    raiz.append(panel(null, null,
      h("div", { class: "reloj" }, h("div", { class: "anillo" }, svg, h("div", { class: "centro" }, tiempoEl, faseEl)),
        h("div", {}, tituloEl, detalleEl, tramos, frasesEl,
          h("div", { class: "fila-botones" }, btnPlay,
            h("button", { class: "btn fantasma", type: "button", onclick: () => ir(idx + 1) }, "Siguiente fase →"),
            h("button", { class: "btn fantasma", type: "button", onclick: () => { pausar(); ir(0); } }, "Reiniciar")),
          h("p", { class: "nota" }, "Atajos: Espacio inicia/pausa · → siguiente fase. Suena un aviso al terminar cada fase.")))));

    function pitido() {
      try { const ctx = new (window.AudioContext || window.webkitAudioContext)(); const o = ctx.createOscillator(); const g = ctx.createGain();
        o.frequency.value = 880; g.gain.setValueAtTime(.15, ctx.currentTime); g.gain.exponentialRampToValueAtTime(.001, ctx.currentTime + .6);
        o.connect(g).connect(ctx.destination); o.start(); o.stop(ctx.currentTime + .6); } catch { /* sin audio */ }
    }
    function pintar() {
      const f = fases[idx]; const total = f.minutos * 60;
      const s = Math.max(0, Math.ceil(restante));
      tiempoEl.textContent = `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
      faseEl.textContent = `Fase ${idx + 1} de ${fases.length}`;
      progreso.style.strokeDashoffset = C * (1 - restante / total);
      tituloEl.textContent = f.nombre; detalleEl.textContent = `${f.minutos} min · ${f.detalle || ""}`;
      [...tramos.children].forEach((t, i) => { t.className = i < idx ? "hecho" : i === idx ? "actual" : ""; });
    }
    function ir(i) {
      if (i >= fases.length) { pausar(); avisar("Clase de prueba completada 🎉"); return; }
      idx = i; restante = fases[i].minutos * 60;
      frasesEl.replaceChildren(...(fases[i].frases || []).map((t) => h("li", {}, t)));
      pintar();
    }
    function tic(t) {
      if (!corriendo) return;
      restante -= (t - ultimo) / 1000; ultimo = t;
      if (restante <= 0) { pitido(); ir(idx + 1); }
      pintar(); raf = requestAnimationFrame(tic);
    }
    function alternar() { corriendo ? pausar() : iniciar(); }
    function iniciar() { corriendo = true; btnPlay.textContent = "Pausar"; ultimo = performance.now(); raf = requestAnimationFrame(tic); }
    function pausar() { corriendo = false; btnPlay.textContent = "Iniciar"; cancelAnimationFrame(raf); }
    document.addEventListener("keydown", (e) => {
      if (e.target.closest("input, textarea")) return;
      if (e.code === "Space") { e.preventDefault(); alternar(); }
      if (e.key === "ArrowRight") ir(idx + 1);
    });
    ir(0);
  }

  // ------------------------------------------------------------ 6. niveles (MCER)
  function niveles(raiz, d) {
    let actual = 0;
    const n = d.niveles.length;
    const escalones = h("div", { class: "escalones", role: "tablist", "aria-label": "Niveles MCER" },
      d.niveles.map((nv, i) => h("button", { type: "button", role: "tab", style: `height:${35 + (65 * i) / Math.max(n - 1, 1)}%;--mezcla:${30 + (70 * i) / Math.max(n - 1, 1)}%`,
        onclick: () => elegir(i) }, nv.nivel)));
    const codigo = h("div", { class: "codigo" }); const nombre = h("h3", { style: "font-size:1.6rem" });
    const desc = h("p", { class: "lead" }); const datos = h("div", { class: "grid tres", style: "margin-top:6px" });
    raiz.append(
      d.verificado ? null : h("p", { class: "nota aviso" }, "⚠ ", d.aviso_verificar),
      panel(null, "Toca un nivel para ver qué significa, cuánto tiempo suele llevar y cuánto inglés usar en clase.",
        escalones, h("div", { class: "detalle-nivel" }, codigo, h("div", { style: "display:grid;gap:10px" }, nombre, desc, datos))),
      h("p", { class: "nota" }, "ⓘ ", d.nota));
    function elegir(i) {
      actual = i; const nv = d.niveles[i];
      [...escalones.children].forEach((b, j) => b.setAttribute("aria-selected", String(j === i)));
      codigo.textContent = nv.nivel; nombre.textContent = nv.nombre; desc.textContent = nv.descripcion;
      datos.replaceChildren(
        h("div", { class: "kpi" }, h("div", { class: "nombre" }, "Horas guiadas (orientativo)"), h("div", { class: "valor", style: "font-size:1.5rem" }, nv.horas || "–")),
        h("div", { class: "kpi" }, h("div", { class: "nombre" }, "Exámenes"), h("div", { class: "valor", style: "font-size:1.2rem" }, nv.examenes || "–")),
        h("div", { class: "kpi destacado" }, h("div", { class: "nombre" }, "Inglés en tus clases"),
          h("div", { class: "valor", style: "font-size:1.4rem" }, nv.ingles || "100% español"), nv.ingles_detalle && h("div", { class: "nombre", style: "margin-top:6px" }, nv.ingles_detalle)));
    }
    document.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") elegir(Math.min(n - 1, actual + 1));
      if (e.key === "ArrowLeft") elegir(Math.max(0, actual - 1));
    });
    elegir(0);
  }

  // ------------------------------------------------------------ 7. tarjetas con audio
  function tarjetas(raiz, d) {
    let mazo = 0, i = 0;
    const pestanas = h("div", { class: "pestanas", role: "tablist" });
    const escena = h("div", { class: "tarjeta-escena" });
    const contador = h("span", { class: "contador" });
    const audio = new Audio();
    const estadoAudio = h("p", { class: "nota oculto" }, "Audio pendiente de generar: ejecuta builder.py materiales --generar");
    audio.addEventListener("error", () => estadoAudio.classList.remove("oculto"));
    const reproducir = (e) => { e.stopPropagation(); estadoAudio.classList.add("oculto"); audio.currentTime = 0; audio.play().catch(() => estadoAudio.classList.remove("oculto")); };
    d.mazos.forEach((m, k) => pestanas.append(h("button", { class: "btn fantasma", type: "button", role: "tab",
      onclick: () => { mazo = k; i = 0; pintar(); } }, m.titulo)));
    raiz.append(panel(null, null, pestanas, h("p", { class: "sub" }), escena, estadoAudio,
      h("div", { class: "navegacion" },
        h("button", { class: "btn fantasma", type: "button", onclick: () => mover(-1) }, "← Anterior"), contador,
        h("button", { class: "btn", type: "button", onclick: () => mover(1) }, "Siguiente →")),
      h("p", { class: "nota" }, "Atajos: Espacio da la vuelta · ← → cambian de tarjeta · A reproduce el audio.")));
    const subtitulo = raiz.querySelector(".sub");
    function pintar() {
      const m = d.mazos[mazo]; const c = m.tarjetas[i];
      [...pestanas.children].forEach((b, k) => b.setAttribute("aria-pressed", String(k === mazo)));
      subtitulo.textContent = m.instruccion;
      audio.src = c.audio;
      const boton = () => h("button", { class: "reproducir", type: "button", "aria-label": "Reproducir audio", onclick: reproducir, html: ICONO_PLAY });
      const frente = m.modo === "listening"
        ? h("div", { class: "cara" }, boton(), h("div", { class: "pista" }, "Escucha. ¿Qué te pregunta el alumno? Toca para ver la respuesta."))
        : h("div", { class: "cara" }, h("div", { class: "frase" }, c.texto), boton(), h("div", { class: "pista" }, "Escucha y repite tres veces. Toca para ver la traducción."));
      const atras = h("div", { class: "cara atras" }, m.modo === "listening" ? h("div", { class: "frase" }, c.texto) : null,
        h("div", { class: m.modo === "listening" ? "pista" : "frase" }, c.traduccion));
      const tarjeta = h("div", { class: "tarjeta", tabindex: 0, role: "button", "aria-label": "Dar la vuelta a la tarjeta",
        onclick: () => tarjeta.classList.toggle("volteada") }, frente, atras);
      escena.replaceChildren(tarjeta);
      contador.textContent = `${i + 1} / ${m.tarjetas.length}`;
      estadoAudio.classList.add("oculto");
    }
    function mover(paso) { const t = d.mazos[mazo].tarjetas.length; i = (i + paso + t) % t; pintar(); }
    document.addEventListener("keydown", (e) => {
      if (e.code === "Space") { e.preventDefault(); escena.querySelector(".tarjeta")?.classList.toggle("volteada"); }
      if (e.key === "ArrowRight") mover(1);
      if (e.key === "ArrowLeft") mover(-1);
      if (e.key.toLowerCase() === "a") reproducir(e);
    });
    pintar();
  }

  // ------------------------------------------------------------ arranque
  const COMPONENTES = { calculadora, diagnostico, hitos, titular, cronometro, niveles, tarjetas };

  function tema() {
    const raiz = document.documentElement;
    const guardado = almacen.leer("swa:tema", null);
    if (guardado) raiz.dataset.theme = guardado;
    const boton = document.querySelector("[data-tema]");
    if (!boton) return;
    boton.addEventListener("click", () => {
      const oscuro = raiz.dataset.theme ? raiz.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
      raiz.dataset.theme = oscuro ? "light" : "dark";
      almacen.guardar("swa:tema", raiz.dataset.theme);
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    tema();
    const nodo = document.getElementById("swa-datos");
    if (!nodo) return;
    const pagina = JSON.parse(nodo.textContent);
    document.querySelectorAll("[data-componente]").forEach((raiz) => {
      const fn = COMPONENTES[raiz.dataset.componente];
      if (fn) fn(raiz, pagina.datos, pagina.id);
      else raiz.append(h("p", { class: "nota aviso" }, `Componente desconocido: ${raiz.dataset.componente}`));
    });
  });
})();
