// main.js — students will add JavaScript here as features are built

// ----- Video modal -----
const modal    = document.getElementById('video-modal');
const iframe   = document.getElementById('demo-iframe');
const openBtn  = document.getElementById('open-demo-btn');
const closeBtn = modal && modal.querySelector('.video-modal-close');
const backdrop = modal && modal.querySelector('.video-modal-backdrop');

function openModal() {
    iframe.src = iframe.dataset.src;
    modal.classList.add('is-open');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    iframe.src = '';
    modal.classList.remove('is-open');
    document.body.style.overflow = '';
}

if (openBtn)  openBtn.addEventListener('click', openModal);
if (closeBtn) closeBtn.addEventListener('click', closeModal);
if (backdrop) backdrop.addEventListener('click', closeModal);

document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modal && modal.classList.contains('is-open')) {
        closeModal();
    }
});
