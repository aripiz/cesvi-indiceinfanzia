/* scroll_top.js — Cesvi Indice Infanzia
   Riporta la pagina in cima ad ogni navigazione interna (SPA).
   Chiude la navbar Bootstrap mobile dopo il click su un link.
   Scroll al click sul chevron hero. */

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

    // ── Scroll al click sullo chevron hero ───────────────────────────────────
    document.addEventListener("click", function (e) {
        const btn = e.target.closest("#hero-scroll-btn");
        if (!btn) return;
        const heroHeight = document.querySelector(".hero-split")?.offsetHeight || window.innerHeight;
        window.scrollTo({ top: heroHeight, behavior: "smooth" });
    });

    // ── Dropdown search placeholder: "Search" → "Cerca" ──────────────────────
    function patchDropdownPlaceholders() {
        document.querySelectorAll("input.dash-dropdown-search").forEach(function (el) {
            if (el.getAttribute("placeholder") !== "Cerca") {
                el.setAttribute("placeholder", "Cerca");
            }
        });
    }
    // Esegui subito e ad ogni mutazione (nuovo nodo o attributo placeholder resettato da React)
    patchDropdownPlaceholders();
    new MutationObserver(patchDropdownPlaceholders).observe(document.body, {
        childList: true, subtree: true,
        attributes: true, attributeFilter: ["placeholder"],
    });
})();
