// Sidebar toggle
function toggleSidebar() {
    const sidebar = document.getElementById('adminSidebar');
    const main = document.getElementById('adminMain');
    sidebar.classList.toggle('open');
}

// Clock
function updateClock() {
    const el = document.getElementById('topbarTime');
    if (el) {
        const now = new Date();
        el.textContent = now.toLocaleTimeString('uz-UZ', {hour:'2-digit', minute:'2-digit'});
    }
}
updateClock();
setInterval(updateClock, 1000);

// Auto-dismiss alerts
setTimeout(() => {
    document.querySelectorAll('.alert').forEach(a => {
        a.style.opacity = '0';
        a.style.transition = 'opacity 0.5s';
        setTimeout(() => a.remove(), 500);
    });
}, 4000);
