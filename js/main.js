// ============================================================
// main.js — comportamento compartilhado de todas as páginas.
// Sem dependências externas: fácil de ler, editar e depurar.
// ============================================================

document.addEventListener("DOMContentLoaded", () => {
  initMobileNav();
  setFooterYear();
  initContactForm();
});

/**
 * Abre/fecha o menu de navegação em telas estreitas.
 */
function initMobileNav() {
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (!toggle || !links) return;

  toggle.addEventListener("click", () => {
    const isOpen = links.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });
}

/**
 * Preenche o ano atual no rodapé (elemento com id="year").
 */
function setFooterYear() {
  const el = document.getElementById("year");
  if (el) el.textContent = new Date().getFullYear();
}

/**
 * Validação simples do formulário de contato.
 * Não envia dados a lugar nenhum ainda — ponto de extensão
 * documentado no README para plugar um backend/serviço de e-mail.
 */
function initContactForm() {
  const form = document.getElementById("contact-form");
  if (!form) return;

  const successBox = document.querySelector(".form-success");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    let hasError = false;

    form.querySelectorAll("[data-required]").forEach((field) => {
      const wrapper = field.closest(".form-field");
      const isEmpty = !field.value.trim();
      const isInvalidEmail =
        field.type === "email" && field.value.trim() && !/^\S+@\S+\.\S+$/.test(field.value);

      if (isEmpty || isInvalidEmail) {
        wrapper.classList.add("has-error");
        hasError = true;
      } else {
        wrapper.classList.remove("has-error");
      }
    });

    if (hasError) return;

    // Ponto de integração futura: enviar `form` via fetch para um
    // endpoint (ex.: Formspree, Resend, backend próprio) aqui.
    form.reset();
    if (successBox) {
      successBox.classList.add("is-visible");
      successBox.setAttribute("tabindex", "-1");
      successBox.focus();
    }
  });
}
