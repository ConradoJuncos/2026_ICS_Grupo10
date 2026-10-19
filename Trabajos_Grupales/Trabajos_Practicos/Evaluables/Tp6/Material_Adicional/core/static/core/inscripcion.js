(() => {
  const activitySelect = document.querySelector("#actividad");
  const activityContent = document.querySelector("#activity-form-content");
  const title = document.querySelector("#registration-title");
  const description = document.querySelector("#registration-description");
  const capacityBadge = document.querySelector("#registration-capacity");
  const capacityValue = document.querySelector("#capacity-value");
  const capacityNote = document.querySelector("#participant-capacity-note");
  const participantCount = document.querySelector("#cantidad-personas");
  const participants = [...document.querySelectorAll("[data-participant]")];
  const sizingFields = [...document.querySelectorAll("[data-sizing-field]")];
  const dateInput = document.querySelector("#fecha-visita");
  const dateFeedback = document.querySelector("#date-feedback");
  const timeSelect = document.querySelector("#horario");
  const termsName = document.querySelector("#terms-activity-name");
  const acceptanceName = document.querySelector("#terms-acceptance-name");
  const terms = document.querySelector("#activity-terms");

  if (!activitySelect || !activityContent) return;

  const options = [...activitySelect.options];
  const initialActivity = new URLSearchParams(window.location.search).get("actividad");

  function resetTimeOptions(placeholder) {
    timeSelect.replaceChildren(new Option(placeholder, "", true, true));
    timeSelect.options[0].disabled = true;
  }

  function refreshTimeOptions() {
    resetTimeOptions("Seleccioná una fecha primero");
    timeSelect.disabled = true;
    dateFeedback.textContent = "Solo se puede reservar dentro de las 24 horas previas al turno y hasta 15 minutos antes de su inicio.";
  }

  function updateParticipants(capacity) {
    const requestedCount = Number(participantCount.value) || 0;
    participants.forEach((participant) => {
      const participantNumber = Number(participant.dataset.participant);
      const isVisible = participantNumber <= requestedCount && participantNumber <= capacity;
      participant.hidden = !isVisible;
      participant.querySelectorAll("input, select").forEach((field) => {
        const sizingField = field.closest("[data-sizing-field]");
        field.disabled = !isVisible || (sizingField !== null && sizingField.hidden);
      });
    });
    if (requestedCount > 0) {
      capacityNote.textContent = `${requestedCount} de ${capacity} cupos máximos seleccionados. Disponibilidad real no conectada.`;
    } else {
      capacityNote.textContent = `Hasta ${capacity} personas por turno. Disponibilidad de muestra; no hay reservas registradas.`;
    }
  }

  function showActivity(option) {
    if (!option || !option.value) {
      activityContent.hidden = true;
      capacityBadge.hidden = true;
      title.textContent = "Inscripción a una actividad.";
      description.textContent = "Elegí una actividad para ver sus horarios, cupos y condiciones.";
      return;
    }

    const activityName = option.textContent.trim();
    const capacity = Number(option.dataset.capacity);
    const requiresSize = option.dataset.requiresSize === "true";
    const minimumAge = Number(option.dataset.minAge);
    const ageGuidance = minimumAge ? `Edad mínima: ${minimumAge} años.` : "Apta para todas las edades.";

    activityContent.hidden = false;
    capacityBadge.hidden = false;
    title.textContent = `Inscripción a ${activityName}.`;
    description.textContent = `${option.dataset.description} ${ageGuidance}`;
    capacityValue.textContent = `${capacity} lugares`;
    participantCount.max = String(capacity);
    participantCount.placeholder = `Entre 1 y ${capacity}`;
    termsName.textContent = activityName;
    acceptanceName.textContent = activityName;
    terms.textContent = option.dataset.terms;

    participants.forEach((participant) => {
      participant.hidden = true;
      participant.querySelectorAll("input, select").forEach((field) => {
        field.disabled = true;
      });
    });
    sizingFields.forEach((field) => {
      field.hidden = !requiresSize;
      const select = field.querySelector("select");
      select.disabled = !requiresSize;
    });
    participantCount.value = "";
    updateParticipants(capacity);
  }

  if (options.some((option) => option.value === initialActivity)) {
    activitySelect.value = initialActivity;
  }
  showActivity(activitySelect.selectedOptions[0]);

  activitySelect.addEventListener("change", () => {
    const url = new URL(window.location.href);
    url.searchParams.set("actividad", activitySelect.value);
    window.history.pushState({}, "", url);
    showActivity(activitySelect.selectedOptions[0]);
    dateInput.value = "";
    refreshTimeOptions();
  });

  window.addEventListener("popstate", () => {
    const activity = new URLSearchParams(window.location.search).get("actividad");
    activitySelect.value = options.some((option) => option.value === activity) ? activity : "";
    showActivity(activitySelect.selectedOptions[0]);
    dateInput.value = "";
    refreshTimeOptions();
  });

  dateInput.addEventListener("change", refreshTimeOptions);
  participantCount.addEventListener("input", () => {
    updateParticipants(Number(participantCount.max));
  });
})();
