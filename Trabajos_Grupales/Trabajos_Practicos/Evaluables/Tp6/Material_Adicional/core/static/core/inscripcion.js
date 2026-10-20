/* El formulario funciona con HTML y el servidor; este código agiliza la carga. */
(() => {
  const formulario = document.querySelector("#registration-form");
  const consulta = document.querySelector("#consulta-turnos");
  if (!formulario || !consulta) return;
  document.documentElement.classList.add("js");

  const alerta = document.querySelector("#form-alert");
  if (alerta) {
    alerta.focus({ preventScroll: true });
    requestAnimationFrame(() => alerta.scrollIntoView({ block: "start" }));
  }

  // Elegir actividad o fecha consulta los turnos sin pasar por un botón.
  function consultar(ancla) {
    const destino = consulta.getAttribute("action").split("#")[0];
    consulta.setAttribute("action", `${destino}#${ancla}`);
    document.body.classList.add("is-loading");
    consulta.submit();
  }

  document.querySelectorAll('input[name="actividad"]').forEach((opcion) => {
    opcion.addEventListener("change", () => {
      document.querySelectorAll('input[name="fecha"]').forEach((fecha) => {
        fecha.checked = false;
      });
      consultar("paso-turno");
    });
  });
  document.querySelectorAll('input[name="fecha"]').forEach((fecha) => {
    fecha.addEventListener("change", () => consultar("horario"));
  });

  const cantidad = document.querySelector("#cantidad-personas");
  if (!cantidad) return;
  const tarjetas = [...document.querySelectorAll("[data-participant]")];
  const nota = document.querySelector("#participant-capacity-note");
  const resumenTurno = document.querySelector('[data-summary="turno"]');
  const resumenPersonas = document.querySelector('[data-summary="personas"]');
  const resumenCompacto = document.querySelector('[data-summary="compacto"]');
  const pasos = [...document.querySelectorAll("[data-step]")];
  const boton = formulario.querySelector(".submit-button");

  const turnoElegido = () => document.querySelector('input[name="horario"]:checked');
  const lugaresDelTurno = () => Number(turnoElegido()?.dataset.cupos || tarjetas.length);
  const personas = (numero) => `${numero} persona${numero === 1 ? "" : "s"}`;

  function mostrarParticipantes({ animar = true } = {}) {
    const lugares = lugaresDelTurno();
    const pedidos = Math.max(0, Math.trunc(Number(cantidad.value)) || 0);
    const visibles = Math.min(pedidos, lugares);
    cantidad.max = String(lugares);

    tarjetas.forEach((tarjeta) => {
      const visible = Number(tarjeta.dataset.participant) <= visibles;
      if (visible && tarjeta.hidden && animar) tarjeta.classList.add("is-entering");
      tarjeta.hidden = !visible;
      tarjeta.querySelectorAll("input, select").forEach((campo) => {
        campo.disabled = !visible;
      });
    });

    if (!turnoElegido()) {
      nota.textContent = "Elegí un turno para ver los lugares disponibles.";
    } else if (pedidos > lugares) {
      nota.textContent = `Este turno tiene ${lugares} lugar${lugares === 1 ? "" : "es"} disponible${lugares === 1 ? "" : "s"}.`;
    } else {
      nota.textContent = `Quedan ${lugares} lugar${lugares === 1 ? "" : "es"} en este turno.`;
    }
    nota.classList.toggle("is-warning", Boolean(turnoElegido()) && pedidos > lugares);
    actualizarResumen(pedidos);
  }

  function actualizarResumen(pedidos) {
    const turno = turnoElegido();
    const hora = turno?.closest("label").querySelector(".choice-title").textContent.trim();
    const fin = hora ? `${String(Number(hora.slice(0, 2)) + 1).padStart(2, "0")}:00` : "";
    if (resumenTurno) resumenTurno.textContent = hora ? `${hora} a ${fin}` : "Sin elegir";
    if (resumenPersonas) resumenPersonas.textContent = personas(pedidos);
    if (resumenCompacto) resumenCompacto.textContent = hora ? `${hora} · ${personas(pedidos)}` : "Elegí fecha y turno";
  }

  function marcarPasos() {
    pasos.forEach((paso) => {
      const campos = [...paso.querySelectorAll("input, select")].filter(
        (campo) => !campo.disabled && campo.type !== "button",
      );
      const completo = campos.length > 0 && campos.every((campo) => campo.checkValidity());
      paso.classList.toggle("is-complete", completo);
    });
  }

  document.querySelectorAll("[data-step-by]").forEach((control) => {
    control.addEventListener("click", () => {
      const actual = Math.trunc(Number(cantidad.value)) || 0;
      const siguiente = Math.min(Math.max(actual + Number(control.dataset.stepBy), 1), lugaresDelTurno());
      cantidad.value = String(siguiente);
      mostrarParticipantes();
      marcarPasos();
    });
  });

  cantidad.addEventListener("input", () => mostrarParticipantes());
  document.querySelectorAll('input[name="horario"]').forEach((turno) => {
    turno.addEventListener("change", () => mostrarParticipantes());
  });
  formulario.addEventListener("input", marcarPasos);
  formulario.addEventListener("change", marcarPasos);
  tarjetas.forEach((tarjeta) => {
    tarjeta.addEventListener("animationend", () => tarjeta.classList.remove("is-entering"));
  });

  formulario.addEventListener("submit", () => {
    boton.disabled = true;
    boton.setAttribute("aria-busy", "true");
    boton.firstChild.textContent = "Confirmando… ";
  });
  window.addEventListener("pageshow", () => {
    boton.disabled = false;
    boton.removeAttribute("aria-busy");
    boton.firstChild.textContent = "Finalizar inscripción ";
    document.body.classList.remove("is-loading");
  });

  mostrarParticipantes({ animar: false });
  marcarPasos();
})();
