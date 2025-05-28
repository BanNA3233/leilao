document.addEventListener("DOMContentLoaded", () => {
    // Scroll suave
    const linksInternos = document.querySelectorAll('a[href^="#"]');
    linksInternos.forEach(link => {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
          window.scrollTo({ top: target.offsetTop - 70, behavior: "smooth" });
        }
      });
    });
  
    // Formulário com feedback animado
    const formContato = document.querySelector(".contato form");
    if (formContato) {
      formContato.addEventListener("submit", (e) => {
        e.preventDefault();
        const feedback = formContato.querySelector(".form-feedback");
        feedback.textContent = "Mensagem enviada com sucesso! ✅";
        feedback.style.opacity = 1;
        setTimeout(() => {
          feedback.style.opacity = 0;
          formContato.reset();
        }, 3000);
      });
    }
  
    // Intersection Observer para animar seções
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }
      });
    }, { threshold: 0.2 });
  
    document.querySelectorAll("section").forEach(sec => observer.observe(sec));
  
    // Botão "voltar ao topo"
    const btnTop = document.getElementById("btnTop");
    window.addEventListener("scroll", () => {
      btnTop.style.display = window.scrollY > 300 ? "block" : "none";
    });
    btnTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  
    // Dark Mode toggle
    const toggleDark = document.getElementById("darkToggle");
    const root = document.body;
    toggleDark?.addEventListener("click", () => {
      const isDark = root.classList.toggle("dark");
      localStorage.setItem("cotaki-theme", isDark ? "dark" : "light");
    });
  
    if (localStorage.getItem("cotaki-theme") === "dark") {
      root.classList.add("dark");
    }
  });
  