// Genera la presentación de la sesión gratuita de 30 min (ES y EN)
// a partir de config.json y contenido.json.
// Uso:  node build_deck.js      Salida: salidas/<archivo definido en contenido.json>
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const BASE = __dirname;
const SALIDAS = path.join(BASE, "salidas");
const { applyTheme } = require("./lib/apply_theme.js");

// Misma paleta que la guía PDF: azul noche + dorado
const HEX = { navy: "14213D", gold: "FCA311", ink: "1B1F2A", muted: "5B6475", soft: "EEF1F6", white: "FFFFFF" };
const THEME = {
  name: "Despega",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: HEX.ink, lt1: HEX.white, dk2: HEX.navy, lt2: HEX.soft,
    accent1: HEX.gold, accent2: HEX.navy, accent3: HEX.muted, accent4: "3BB273", accent5: "E76F51", accent6: "8D99AE",
    hlink: HEX.gold, folHlink: HEX.muted,
  },
};

const W = 10, H = 5.625, M = 0.5;

function rellenar(texto, valores) {
  return Object.entries(valores).reduce((t, [k, v]) => t.split(`{${k}}`).join(v), texto);
}

async function construir(lang, contenido, cfg) {
  const deck = contenido[lang].deck;
  const valores = {
    nombre: cfg.nombre, contacto: cfg.contacto,
    fecha_limite: cfg[`fecha_limite_${lang}`], precio_programa: cfg.precio_programa,
  };
  const R = (t) => rellenar(t, valores);
  const s = deck.slides;

  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  pres.author = cfg.nombre;
  pres.title = R(s.portada.titulo);
  const C = pres.SchemeColor;

  // ---- Layouts ----
  pres.defineSlideMaster({
    title: "OSCURO",
    background: { color: C.text2 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: M, y: 0.45, w: 6.8, h: 1.1, fontFace: THEME.headFontFace, fontSize: 30, bold: true, color: C.background1, align: "left", valign: "top", margin: 0 }, text: "" } },
    ],
  });
  pres.defineSlideMaster({
    title: "CLARO",
    background: { color: C.background1 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: M, y: 0.35, w: W - 2 * M, h: 0.75, fontFace: THEME.headFontFace, fontSize: 30, bold: true, color: C.text2, align: "left", valign: "middle", margin: 0 }, text: "" } },
    ],
    slideNumber: { x: W - 0.9, y: H - 0.4, w: 0.5, h: 0.25, fontSize: 10, color: C.accent3, align: "right" },
  });

  // Motivo visual: anillo dorado (igual que la portada del PDF)
  const anillo = (slide, x, y, d) => {
    slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: C.accent1 }, line: { type: "none" }, objectName: "Anillo exterior" });
    const t = d * 0.2;
    slide.addShape(pres.shapes.OVAL, { x: x + t, y: y + t, w: d - 2 * t, h: d - 2 * t, fill: { color: C.text2 }, line: { type: "none" }, objectName: "Anillo interior" });
  };
  const numero = (slide, n, x, y, d = 0.5) => {
    slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: C.accent1 }, line: { type: "none" }, objectName: `Círculo ${n}` });
    slide.addText(String(n), { x, y, w: d, h: d, align: "center", valign: "middle", fontFace: THEME.headFontFace, fontSize: 18, bold: true, color: C.text2, margin: 0, isTextBox: true });
  };
  const tarjeta = (slide, x, y, w, h, nombre) =>
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: C.background2 }, line: { type: "none" }, objectName: nombre });

  // 1. Portada
  pres.addSection({ title: lang === "es" ? "Apertura" : "Opening" });
  let sl = pres.addSlide({ masterName: "OSCURO", sectionTitle: lang === "es" ? "Apertura" : "Opening" });
  anillo(sl, 6.6, -1.2, 4.6);
  sl.addText(R(s.portada.titulo), { x: M, y: 1.7, w: 6.2, h: 1.4, fontFace: THEME.headFontFace, fontSize: 40, bold: true, color: C.background1, valign: "bottom", margin: 0, isTextBox: true });
  sl.addText(R(s.portada.subtitulo), { x: M, y: 3.2, w: 6.2, h: 0.6, fontSize: 18, color: C.background2, margin: 0, isTextBox: true });
  sl.addText(R(s.portada.por), { x: M, y: H - 0.9, w: 5, h: 0.4, fontSize: 16, bold: true, color: C.accent1, margin: 0, isTextBox: true });
  sl.addNotes(R(s.portada.notas));

  // 2. Agenda
  sl = pres.addSlide({ masterName: "CLARO", sectionTitle: lang === "es" ? "Apertura" : "Opening" });
  sl.addText(R(s.agenda.titulo), { placeholder: "title" });
  s.agenda.items.forEach(([min, txt], i) => {
    const y = 1.3 + i * 0.75;
    sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y, w: 1.2, h: 0.5, rectRadius: 0.25, fill: { color: C.accent1 }, line: { type: "none" }, objectName: `Tiempo ${i + 1}` });
    sl.addText(min, { x: M, y, w: 1.2, h: 0.5, align: "center", valign: "middle", fontSize: 16, bold: true, color: C.text2, margin: 0, isTextBox: true });
    sl.addText(R(txt), { x: M + 1.5, y, w: 6.5, h: 0.5, valign: "middle", fontSize: 18, color: C.text1, margin: 0, isTextBox: true });
  });
  anillo(sl, 7.6, 1.9, 2.0);
  sl.addNotes(R(s.agenda.notas));

  // 3. Historia (estadísticas)
  sl = pres.addSlide({ masterName: "CLARO", sectionTitle: lang === "es" ? "Apertura" : "Opening" });
  sl.addText(R(s.historia.titulo), { placeholder: "title" });
  const sw = (W - 2 * M - 2 * 0.3) / 3;
  s.historia.stats.forEach(([num, lbl], i) => {
    const x = M + i * (sw + 0.3);
    tarjeta(sl, x, 1.4, sw, 2.6, `Dato ${i + 1}`);
    sl.addText(num, { x: x + 0.25, y: 1.7, w: sw - 0.5, h: 1.0, fontFace: THEME.headFontFace, fontSize: 34, bold: true, color: C.text2, margin: 0, isTextBox: true });
    sl.addText(R(lbl), { x: x + 0.25, y: 2.8, w: sw - 0.5, h: 0.9, fontSize: 16, color: C.accent3, valign: "top", margin: 0, isTextBox: true });
  });
  sl.addText(R(s.historia.nota), { x: M, y: 4.4, w: 7, h: 0.35, fontSize: 11, italic: true, color: C.accent3, margin: 0, isTextBox: true });
  sl.addNotes(R(s.historia.notas));

  // 4. Por qué Preply (2x2)
  pres.addSection({ title: lang === "es" ? "Perfil" : "Profile" });
  sl = pres.addSlide({ masterName: "CLARO", sectionTitle: lang === "es" ? "Perfil" : "Profile" });
  sl.addText(R(s.porque.titulo), { placeholder: "title" });
  const cw = (W - 2 * M - 0.3) / 2;
  s.porque.tarjetas.forEach(([t, d], i) => {
    const x = M + (i % 2) * (cw + 0.3), y = 1.3 + Math.floor(i / 2) * 1.75;
    tarjeta(sl, x, y, cw, 1.5, `Ventaja ${i + 1}`);
    numero(sl, i + 1, x + 0.25, y + 0.3);
    sl.addText(R(t), { x: x + 0.95, y: y + 0.22, w: cw - 1.2, h: 0.45, fontSize: 18, bold: true, color: C.text2, margin: 0, isTextBox: true });
    sl.addText(R(d), { x: x + 0.95, y: y + 0.68, w: cw - 1.2, h: 0.7, fontSize: 14, color: C.text1, valign: "top", margin: 0, isTextBox: true });
  });
  sl.addNotes(R(s.porque.notas));

  // 5. Tres pilares del perfil
  sl = pres.addSlide({ masterName: "CLARO", sectionTitle: lang === "es" ? "Perfil" : "Profile" });
  sl.addText(R(s.perfil.titulo), { placeholder: "title" });
  s.perfil.tarjetas.forEach(([t, d], i) => {
    const x = M + i * (sw + 0.3);
    tarjeta(sl, x, 1.35, sw, 3.4, `Pilar ${i + 1}`);
    numero(sl, i + 1, x + 0.3, 1.65, 0.6);
    sl.addText(R(t), { x: x + 0.3, y: 2.45, w: sw - 0.6, h: 0.5, fontFace: THEME.headFontFace, fontSize: 22, bold: true, color: C.text2, margin: 0, isTextBox: true });
    sl.addText(R(d), { x: x + 0.3, y: 3.0, w: sw - 0.6, h: 1.6, fontSize: 14, color: C.text1, valign: "top", margin: 0, isTextBox: true });
  });
  sl.addNotes(R(s.perfil.notas));

  // 6. Título: antes y después
  sl = pres.addSlide({ masterName: "CLARO", sectionTitle: lang === "es" ? "Perfil" : "Profile" });
  sl.addText(R(s.titular.titulo), { placeholder: "title" });
  const bw = 3.7;
  tarjeta(sl, M, 1.45, bw, 2.2, "Antes");
  sl.addText(R(s.titular.antes_label).toUpperCase(), { x: M + 0.3, y: 1.65, w: bw - 0.6, h: 0.35, fontSize: 12, bold: true, color: C.accent3, charSpacing: 2, margin: 0, isTextBox: true });
  sl.addText(R(s.titular.antes), { x: M + 0.3, y: 2.05, w: bw - 0.6, h: 1.4, fontSize: 20, color: C.accent3, strike: "sngStrike", valign: "top", margin: 0, isTextBox: true });
  sl.addShape(pres.shapes.RIGHT_ARROW, { x: M + bw + 0.2, y: 2.3, w: 0.7, h: 0.5, fill: { color: C.accent1 }, line: { type: "none" }, objectName: "Flecha" });
  const ax = M + bw + 1.1;
  sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: ax, y: 1.45, w: W - M - ax, h: 2.2, rectRadius: 0.08, fill: { color: C.text2 }, line: { type: "none" }, objectName: "Después" });
  sl.addText(R(s.titular.despues_label).toUpperCase(), { x: ax + 0.3, y: 1.65, w: W - M - ax - 0.6, h: 0.35, fontSize: 12, bold: true, color: C.accent1, charSpacing: 2, margin: 0, isTextBox: true });
  sl.addText(R(s.titular.despues), { x: ax + 0.3, y: 2.05, w: W - M - ax - 0.6, h: 1.45, fontSize: 18, bold: true, color: C.background1, valign: "top", margin: 0, isTextBox: true });
  sl.addText(R(s.titular.formula), { x: M, y: 4.05, w: W - 2 * M, h: 0.5, fontSize: 18, italic: true, color: C.text2, margin: 0, isTextBox: true });
  sl.addNotes(R(s.titular.notas));

  // 7. Precio por etapas (escalera)
  pres.addSection({ title: lang === "es" ? "Precio y clase de prueba" : "Pricing and trial lesson" });
  const secPrecio = lang === "es" ? "Precio y clase de prueba" : "Pricing and trial lesson";
  sl = pres.addSlide({ masterName: "CLARO", sectionTitle: secPrecio });
  sl.addText(R(s.precio.titulo), { placeholder: "title" });
  s.precio.etapas.forEach(([t, d], i) => {
    const x = M + i * (sw + 0.3), alto = 1.65 + i * 0.65, y = 4.95 - alto;
    sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: sw, h: alto, rectRadius: 0.08, fill: { color: i === 2 ? C.text2 : C.background2 }, line: { type: "none" }, objectName: `Etapa ${i + 1}` });
    sl.addText(R(t), { x: x + 0.25, y: y + 0.2, w: sw - 0.5, h: 0.4, fontSize: 18, bold: true, color: i === 2 ? C.accent1 : C.text2, margin: 0, isTextBox: true });
    sl.addText(R(d), { x: x + 0.25, y: y + 0.65, w: sw - 0.5, h: alto - 0.8, fontSize: 14, color: i === 2 ? C.background1 : C.text1, valign: "top", margin: 0, isTextBox: true });
  });
  sl.addNotes(R(s.precio.notas));

  // 8. Clase de prueba (proceso de 4 pasos)
  sl = pres.addSlide({ masterName: "CLARO", sectionTitle: secPrecio });
  sl.addText(R(s.prueba.titulo), { placeholder: "title" });
  const pw = (W - 2 * M) / 4;
  sl.addShape(pres.shapes.LINE, { x: M + pw / 2, y: 1.95, w: pw * 3, h: 0, line: { color: C.accent1, width: 3 }, objectName: "Conector" });
  s.prueba.pasos.forEach(([t, d], i) => {
    const cx = M + i * pw + pw / 2;
    numero(sl, i + 1, cx - 0.35, 1.6, 0.7);
    sl.addText(R(t), { x: cx - pw / 2 + 0.1, y: 2.55, w: pw - 0.2, h: 0.45, align: "center", fontSize: 18, bold: true, color: C.text2, margin: 0, isTextBox: true });
    sl.addText(R(d), { x: cx - pw / 2 + 0.15, y: 3.05, w: pw - 0.3, h: 1.2, align: "center", fontSize: 14, color: C.text1, valign: "top", margin: 0, isTextBox: true });
  });
  sl.addNotes(R(s.prueba.notas));

  // 9. Primeras 2 semanas (línea de tiempo)
  pres.addSection({ title: lang === "es" ? "Cierre" : "Closing" });
  const secCierre = lang === "es" ? "Cierre" : "Closing";
  sl = pres.addSlide({ masterName: "CLARO", sectionTitle: secCierre });
  sl.addText(R(s.plan.titulo), { placeholder: "title" });
  s.plan.fases.forEach(([t, d], i) => {
    const y = 1.35 + i * 1.15;
    tarjeta(sl, M, y, W - 2 * M, 0.95, `Fase ${i + 1}`);
    sl.addText(R(t), { x: M + 0.3, y, w: 1.9, h: 0.95, valign: "middle", fontFace: THEME.headFontFace, fontSize: 20, bold: true, color: C.text2, margin: 0, isTextBox: true });
    sl.addShape(pres.shapes.OVAL, { x: M + 2.3, y: y + 0.36, w: 0.24, h: 0.24, fill: { color: C.accent1 }, line: { type: "none" }, objectName: `Hito ${i + 1}` });
    sl.addText(R(d), { x: M + 2.8, y, w: W - 2 * M - 3.1, h: 0.95, valign: "middle", fontSize: 17, color: C.text1, margin: 0, isTextBox: true });
  });
  sl.addNotes(R(s.plan.notas));

  // 10. Programa de pago
  sl = pres.addSlide({ masterName: "OSCURO", sectionTitle: secCierre });
  sl.addText(R(s.programa.titulo), { placeholder: "title", w: W - 2 * M });
  sl.addText(s.programa.items.map((t, i, arr) => ({ text: R(t), options: { bullet: { indent: 18 }, breakLine: i < arr.length - 1, paraSpaceAfter: 10 } })),
    { x: M, y: 1.85, w: 5.6, h: 3.0, fontSize: 17, color: C.background1, valign: "top", margin: 0, isTextBox: true });
  sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.6, y: 1.85, w: 2.9, h: 2.4, rectRadius: 0.1, fill: { color: C.accent1 }, line: { type: "none" }, objectName: "Precio" });
  sl.addText(R(s.programa.precio_label), { x: 6.6, y: 2.1, w: 2.9, h: 0.4, align: "center", fontSize: 15, bold: true, color: C.text2, margin: 0, isTextBox: true });
  sl.addText(R(s.programa.precio), { x: 6.6, y: 2.55, w: 2.9, h: 1.3, align: "center", valign: "middle", fontFace: THEME.headFontFace, fontSize: 54, bold: true, color: C.text2, margin: 0, isTextBox: true });
  sl.addNotes(R(s.programa.notas));

  // 11. Próximos pasos
  sl = pres.addSlide({ masterName: "OSCURO", sectionTitle: secCierre });
  sl.addText(R(s.cierre.titulo), { placeholder: "title" });
  anillo(sl, 7.2, 0.5, 2.3);
  s.cierre.items.forEach((t, i) => {
    const y = 1.55 + i * 0.8;
    numero(sl, i + 1, M, y, 0.55);
    sl.addText(R(t), { x: M + 0.8, y, w: 6.0, h: 0.55, valign: "middle", fontSize: 18, color: C.background1, margin: 0, isTextBox: true });
  });
  sl.addText(R(s.cierre.contacto), { x: M, y: 4.1, w: 6, h: 0.4, fontSize: 16, bold: true, color: C.accent1, margin: 0, isTextBox: true });
  sl.addText(R(s.cierre.transparencia), { x: M, y: 4.6, w: W - 2 * M, h: 0.6, fontSize: 10, italic: true, color: C.background2, valign: "top", margin: 0, isTextBox: true });
  sl.addNotes(R(s.cierre.notas));

  fs.mkdirSync(SALIDAS, { recursive: true });
  const salida = path.join(SALIDAS, deck.archivo);
  await pres.writeFile({ fileName: salida });
  // pptxgenjs no escribe los colores del tema; sin esto saldría la paleta azul de Office
  await applyTheme(salida, THEME);
  console.log(`OK  ${salida}`);
}

(async () => {
  const cfg = JSON.parse(fs.readFileSync(path.join(BASE, "config.json"), "utf8"));
  const contenido = JSON.parse(fs.readFileSync(path.join(BASE, "contenido.json"), "utf8"));
  for (const lang of ["es", "en"]) await construir(lang, contenido, cfg);
})();
