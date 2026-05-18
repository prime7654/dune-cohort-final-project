(function () {
    "use strict";

    function markImageState(image, stateClass) {
        var frame = image.closest(".image-skeleton");
        if (!frame) {
            return;
        }
        frame.classList.add(stateClass);
    }

    function initImageSkeletons() {
        document.querySelectorAll(".js-skeleton-image").forEach(function (image) {
            if (image.complete) {
                markImageState(image, image.naturalWidth > 0 ? "is-loaded" : "has-error");
                return;
            }

            if (image.dataset.skeletonBound === "true") {
                return;
            }

            image.dataset.skeletonBound = "true";
            image.addEventListener("load", function () {
                markImageState(image, "is-loaded");
            }, { once: true });
            image.addEventListener("error", function () {
                markImageState(image, "has-error");
            }, { once: true });
        });
    }

    function currentPageKind() {
        var pageMarker = document.querySelector("[data-skeleton-page]");
        return pageMarker ? pageMarker.getAttribute("data-skeleton-page") : "";
    }

    function routeKindFromUrl(url) {
        var path = url.pathname.replace(/\/+$/, "/");

        if (path.endsWith("/menu_list/")) {
            return "menu";
        }

        if (path.endsWith("/dashboard/")) {
            return "dashboard";
        }

        return "";
    }

    function clearRouteSkeleton() {
        document.body.classList.remove("is-page-transitioning");
        document.body.removeAttribute("data-route-skeleton");

        var main = document.querySelector(".site-main");
        if (main) {
            main.removeAttribute("aria-busy");
        }
    }

    function showRouteSkeleton(kind) {
        if (!kind || !document.querySelector("[data-route-skeleton]")) {
            return;
        }

        document.body.setAttribute("data-route-skeleton", kind);
        document.body.classList.add("is-page-transitioning");

        var main = document.querySelector(".site-main");
        if (main) {
            main.setAttribute("aria-busy", "true");
        }
    }

    document.addEventListener("click", function (event) {
        if (
            event.defaultPrevented ||
            event.button !== 0 ||
            event.metaKey ||
            event.ctrlKey ||
            event.shiftKey ||
            event.altKey
        ) {
            return;
        }

        var link = event.target.closest("a[href]");
        if (!link || link.hasAttribute("download") || (link.target && link.target !== "_self")) {
            return;
        }

        var href = link.getAttribute("href");
        if (!href || href.charAt(0) === "#") {
            return;
        }

        var url;
        try {
            url = new URL(link.href, window.location.href);
        } catch (error) {
            return;
        }

        if (url.origin !== window.location.origin) {
            return;
        }

        if (url.pathname === window.location.pathname && url.search === window.location.search) {
            return;
        }

        showRouteSkeleton(link.getAttribute("data-skeleton-link") || routeKindFromUrl(url));
    }, true);

    document.addEventListener("submit", function (event) {
        if (event.defaultPrevented) {
            return;
        }

        var form = event.target;
        if (!(form instanceof HTMLFormElement) || (form.target && form.target !== "_self")) {
            return;
        }

        showRouteSkeleton(form.getAttribute("data-skeleton-link") || currentPageKind());
    }, true);

    document.addEventListener("DOMContentLoaded", function () {
        clearRouteSkeleton();
        initImageSkeletons();
    });

    window.addEventListener("pageshow", function () {
        clearRouteSkeleton();
        initImageSkeletons();
    });
}());
