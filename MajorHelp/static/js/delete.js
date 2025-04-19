document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("confirm-modal");
    const confirmMessage = document.getElementById("confirm-message");
    const confirmYes = document.getElementById("confirm-yes");
    const confirmNo = document.getElementById("confirm-no");

    let targetForm = null;

    document.querySelectorAll(".delete-confirm").forEach(button => {
        button.addEventListener("click", e => {
            e.preventDefault();
            targetForm = button.closest("form");
            const item = button.dataset.item || "this item";
            confirmMessage.textContent = `Are you sure you want to delete ${item}? This action cannot be undone.`;
            modal.style.display = "flex";
        });
    });

    confirmYes.addEventListener("click", () => {
        if (targetForm) targetForm.submit();
    });

    confirmNo.addEventListener("click", () => {
        modal.style.display = "none";
        targetForm = null;
    });
});
