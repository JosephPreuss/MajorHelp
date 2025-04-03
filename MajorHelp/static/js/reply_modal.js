document.addEventListener("DOMContentLoaded", function () {
    const fab = document.getElementById("fab-reply");
    const modal = document.getElementById("reply-modal");
    const closeBtn = document.getElementById("close-modal");

    if (fab && modal) {
        fab.addEventListener("click", () => {
            modal.classList.add("active");
        });

        closeBtn?.addEventListener("click", () => {
            modal.classList.remove("active");
        });

        // Optional: close modal when clicking outside of it
        window.addEventListener("click", (e) => {
            if (e.target === modal) {
                modal.classList.remove("active");
            }
        });
    }
});
