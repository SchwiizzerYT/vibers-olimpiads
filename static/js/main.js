// Hamburger menu
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');
if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => navMenu.classList.toggle('open'));
}

// Password toggle
function togglePassword(id, btn) {
    const inp = document.getElementById(id);
    if (inp.type === 'password') {
        inp.type = 'text';
        btn.innerHTML = '<i class="fas fa-eye-slash"></i>';
    } else {
        inp.type = 'password';
        btn.innerHTML = '<i class="fas fa-eye"></i>';
    }
}

// Auto-dismiss alerts
setTimeout(() => {
    document.querySelectorAll('.alert').forEach(a => {
        a.style.opacity = '0';
        a.style.transition = 'opacity 0.5s';
        setTimeout(() => a.remove(), 500);
    });
}, 5000);

// Modal functions
function showRegisterModal() {
    document.getElementById('registerModal').style.display = 'flex';
}
function closeModal() {
    document.getElementById('registerModal').style.display = 'none';
}
