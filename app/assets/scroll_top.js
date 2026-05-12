/* scroll_top.js — Cesvi Indice Infanzia
   Riporta la pagina in cima ad ogni navigazione interna (SPA).
   Chiude la navbar Bootstrap mobile dopo il click su un link. */

(function () {
    "use strict";

    // ── Scroll to top on navigation ──────────────────────────────────────────
    const originalPushState = history.pushState.bind(history);
    history.pushState = function (...args) {
        originalPushState(...args);
        window.scrollTo({ top: 0, behavior: "instant" });
    };

    window.addEventListener("popstate", function () {
        window.scrollTo({ top: 0, behavior: "instant" });
    });

    // ── Chiudi navbar mobile dopo click su link ───────────────────────────────
    document.addEventListener("click", function (e) {
        const link = e.target.closest(".navbar-nav .nav-link");
        if (!link) return;
        const collapse = document.querySelector(".navbar-collapse.show");
        if (!collapse) return;
        // Usa Bootstrap collapse API se disponibile, altrimenti rimuovi classe
        if (window.bootstrap && window.bootstrap.Collapse) {
            const bsCollapse = window.bootstrap.Collapse.getInstance(collapse);
            if (bsCollapse) {
                bsCollapse.hide();
            } else {
                collapse.classList.remove("show");
            }
        } else {
            collapse.classList.remove("show");
        }
    });
})();
