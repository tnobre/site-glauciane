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
 * Validação e envio do formulário de contato.
 *
 * O envio vai para o Netlify Forms: a Netlify identifica o formulário
 * pelo atributo `data-netlify` no HTML e recebe um POST na própria raiz
 * do site — não existe backend nem chave de API para manter. Os envios
 * ficam no painel da Netlify e são notificados por e-mail.
 */
function initContactForm() {
  const form = document.getElementById("contact-form");
  if (!form) return;

  const successBox = document.querySelector(".form-success");
  const failureBox = document.querySelector(".form-falha");
  const submitButton = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", async (event) => {
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

    const rotuloOriginal = submitButton ? submitButton.textContent : "";
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = "Enviando...";
    }
    if (failureBox) failureBox.classList.remove("is-visible");

    try {
      const resposta = await fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(new FormData(form)).toString(),
      });
      if (!resposta.ok) throw new Error("HTTP " + resposta.status);

      form.reset();
      if (successBox) {
        successBox.classList.add("is-visible");
        successBox.setAttribute("tabindex", "-1");
        successBox.focus();
      }
    } catch (erro) {
      // Falha de rede ou erro da Netlify: o texto preenchido é mantido
      // para a pessoa não perder o que escreveu e poder tentar de novo.
      console.error("Falha ao enviar o formulário:", erro);
      if (failureBox) {
        failureBox.classList.add("is-visible");
        failureBox.setAttribute("tabindex", "-1");
        failureBox.focus();
      }
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.textContent = rotuloOriginal;
      }
    }
  });
}
