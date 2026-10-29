# Kit de referidos Preply: sesión gratis de 30 min

Material para atraer tutores de materias que no sean idiomas a Preply con tu enlace de referido, en español e inglés.

## Qué hay aquí

| Archivo | Para qué sirve |
|---|---|
| `salidas/Guia-Ensena-Tu-Materia-ES.pdf` / `salidas/Guide-Teach-Your-Subject-EN.pdf` | Guía gratuita (lead magnet). Se comparte en redes, grupos y anuncios. Botones clicables: registro con tu enlace y reserva en TidyCal. |
| `salidas/Sesion-Gratis-30min-ES.pptx` / `salidas/Free-30min-Session-EN.pptx` | Presentación para la sesión de 30 min. Cada diapositiva trae **notas del presentador** con lo que debes decir y hacer. |
| `config.json` | **Tus datos:** nombre, enlaces de TidyCal, email y precio del programa. |
| `contenido.json` | Todos los textos de la guía y de la presentación, en los dos idiomas. |

## Cómo cambiar tus datos y volver a generar todo

1. Edita `config.json` (tu nombre, tus enlaces reales de TidyCal, tu email y el precio).
2. Ejecuta lo siguiente (requiere Python 3 con `reportlab` y Node.js):

```bash
cd referidos && npm install && npm run build
```

Los archivos nuevos aparecen en `salidas/`.

---

## El flujo

```
Post, video o anuncio → descarga la guía PDF
   → Paso 1: se registra en Preply con TU enlace
   → Paso 2: reserva su sesión gratis en TidyCal (con el email con el que se registró)
   → Paso 3: videollamada de 30 min (usas la presentación)
   → Opcional: compra el programa «Despega en Preply»
```

> Preply no muestra todavía tus referidos en el panel, así que TidyCal se convierte en **tu registro**: cada reserva guarda nombre, email, materia y nacionalidad.

---

## Configuración de TidyCal Pro (copiar y pegar)

Crea **dos tipos de reserva**, una por idioma. Configuración común:

| Ajuste | Valor |
|---|---|
| Duración | 30 minutos |
| Precio | Gratis |
| Ubicación | Google Meet o Zoom (enlace automático) |
| Calendario | Revisión de conflictos con tu Google Calendar ✅ |
| Margen antes/después | 10 min |
| Aviso mínimo | 12 horas |
| Máximo por día | 3 |
| Horarios | Solo tus bloques libres de Preply |

### Tipo de reserva en español

**URL:** `sesion-gratis-30`

**Título:** Sesión gratis de 30 min: empieza a enseñar tu materia en Preply

**Descripción:**
> Sesión 1 a 1 de 30 minutos para tutores nuevos de materias que no sean idiomas (matemáticas, música, ciencias, programación y más).
>
> **Antes de reservar:** regístrate como tutor en Preply con mi enlace. Esta sesión es exclusiva para quienes se unen a través de él.
>
> 👉 Regístrate aquí: https://preply.com/en/teach?utm_source=friend_raf&utm_medium=landing_page&utm_campaign=tut_raf_raf_all_0_mul_xx_multiplesub_exp-target-raf-pilot-75622_0_bau
>
> En la sesión revisamos tu perfil, tu video, tu precio de arranque y tu plan para las primeras 2 semanas.
>
> *Transparencia: Preply me paga un bono si te registras con mi enlace y das tu primera clase de suscripción. A ti no te cuesta nada.*

**Preguntas del formulario:**
1. ¿Con qué email te registraste en Preply? *(obligatoria)*
2. ¿Te registraste como tutor usando mi enlace? *(obligatoria: Sí / Todavía no)*
3. ¿Tienes nacionalidad de EE. UU. o del Reino Unido? *(obligatoria: EE. UU. / Reino Unido / Ninguna)*
4. ¿Qué materia vas a enseñar? *(obligatoria)*
5. ¿Qué es lo que más te gustaría resolver en la sesión? *(opcional)*

**Mensaje de confirmación:**
> ¡Listo! Tu sesión está reservada. Te llegará un email con el enlace de la videollamada.
> Para aprovecharla al máximo, ten abierto tu perfil de Preply (aunque esté a medias) y piensa en el título que te gustaría tener. ¡Nos vemos!

### Tipo de reserva en inglés

**URL:** `free-30-min-session`

**Title:** Free 30-min session: start teaching your subject on Preply

**Description:**
> A 30-minute 1:1 session for new tutors of non-language subjects (math, music, science, coding and more).
>
> **Before booking:** sign up as a tutor on Preply with my link. This session is only for people who join through it.
>
> 👉 Sign up here: https://preply.com/en/teach?utm_source=friend_raf&utm_medium=landing_page&utm_campaign=tut_raf_raf_all_0_mul_xx_multiplesub_exp-target-raf-pilot-75622_0_bau
>
> We'll review your profile, your intro video, your starting price and your plan for the first 2 weeks.
>
> *Disclosure: Preply pays me a bonus if you sign up with my link and teach your first subscription lesson. It costs you nothing.*

**Booking questions:**
1. What email did you use to sign up on Preply? *(required)*
2. Did you sign up as a tutor using my link? *(required: Yes / Not yet)*
3. Do you hold US or UK nationality? *(required: US / UK / Neither)*
4. What subject will you teach? *(required)*
5. What would you most like to solve in the session? *(optional)*

**Confirmation message:**
> You're all set! You'll get an email with the video call link.
> To get the most out of it, have your Preply profile open (even if it's unfinished) and think about the headline you'd like. See you soon!

### Si alguien reserva sin cumplir los requisitos

- **Respondió «Todavía no»:** escríbele antes de la sesión con tu enlace y pídele que se registre. Si no lo hace, cancela con amabilidad.
- **Respondió «Ninguna» en nacionalidad:** no genera bono, pero ofrécele el programa de pago.

---

## Reglas para no poner en riesgo tu cuenta

- ❌ No compartas este material ni tu TidyCal por el chat de Preply ni durante tus clases.
- ❌ No prometas ingresos. Presenta tus números como tu caso personal.
- ❌ No registres cuentas falsas ni a personas que no vayan a enseñar.
- ✅ Incluye siempre la nota de transparencia (lo exige la FTC en EE. UU.).
- ⚠️ Revisa los [términos del programa](https://termsofuse.preply.com/terms_of_use/en_ReferralProgramTermsAndConditionsFile.pdf), sobre todo si permiten condicionar un beneficio propio al uso del enlace y hacer publicidad pagada.
