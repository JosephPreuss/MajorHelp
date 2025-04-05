document.addEventListener('DOMContentLoaded', function () {
    const fabButton = document.getElementById('fab-reply');
    const replyModal = document.getElementById('reply-modal');
    const modalOverlay = document.getElementById('modal-overlay');
    const closeModalBtn = document.getElementById('close-modal');
    const blurWrapper = document.getElementById('thread-blur-wrapper');

    function showModal() {
        replyModal.classList.add('active');
        modalOverlay.classList.add('active');
        blurWrapper.classList.add('modal-blur');
    }

    function hideModal() {
        replyModal.classList.remove('active');
        modalOverlay.classList.remove('active');
        blurWrapper.classList.remove('modal-blur');
    }

    fabButton?.addEventListener('click', showModal);
    closeModalBtn?.addEventListener('click', hideModal);
    modalOverlay?.addEventListener('click', hideModal);
});
