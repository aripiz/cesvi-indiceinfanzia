/* scroll_top.js — Cesvi Indice Infanzia
   Riporta la pagina in cima ad ogni navigazione interna (SPA). */

(function () {
    "use strict";

    // Osserva il cambio di pathname via History API
    const originalPushState = history.pushState.bind(history);
    history.pushState = function (...args) {
        originalPushState(...args);
        window.scrollTo({ top: 0, behavior: "instant" });
    };

    window.addEventListener("popstate", function () {
        window.scrollTo({ top: 0, behavior: "instant" });
    });
})();
