// Menunggu sampai semua konten HTML dimuat
document.addEventListener('DOMContentLoaded', () => {

    // Ambil semua link di sidebar
    const sidebarLinks = document.querySelectorAll('.sidebar ul li a');

    // Fungsi untuk menangani klik
    function handleLinkClick(e) {
        // Hapus kelas 'active' dari SEMUA link
        sidebarLinks.forEach(link => {
            link.classList.remove('active');
        });

        // Tambahkan kelas 'active' hanya ke link yang BARU DIKLIK
        this.classList.add('active');
    }

    // Tambahkan event listener 'click' ke setiap link
    sidebarLinks.forEach(link => {
        link.addEventListener('click', handleLinkClick);
    });

});