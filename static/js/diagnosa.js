document.addEventListener("DOMContentLoaded", () => {

    /* ============================================================
       1. TOGGLE CARD
    ============================================================ */
    const symptomCards = document.querySelectorAll(".symptom-card");

    symptomCards.forEach(card => {
        card.addEventListener("click", (e) => {
            e.preventDefault();

            const checkbox = card.previousElementSibling;
            checkbox.checked = !checkbox.checked;
            card.classList.toggle("selected");
        });
    });



    /* ============================================================
       2. FILTER & SEARCH
    ============================================================ */
    const filterButtons = document.querySelectorAll(".filter-btn");
    const searchInput = document.querySelector(".search-bar input");
    const symptomItems = document.querySelectorAll(".symptom-item");

    let activeFilter = "all";

    filterButtons.forEach(btn => {
        btn.addEventListener("click", () => {

            document.querySelector(".filter-btn.active").classList.remove("active");
            btn.classList.add("active");

            activeFilter = btn.dataset.filter.toLowerCase();
            filterSymptoms();
        });
    });

    searchInput.addEventListener("keyup", () => {
        filterSymptoms();
    });

    function filterSymptoms() {
        const searchTerm = searchInput.value.toLowerCase();

        symptomItems.forEach(item => {

            const kategori = item.dataset.kategori.toLowerCase();
            const name = item.querySelector(".symptom-name").textContent.toLowerCase();

            const matchSearch = name.includes(searchTerm);
            const matchFilter = activeFilter === "all" || kategori === activeFilter;

            // PENTING: gunakan "", bukan "block"
            item.style.display = (matchSearch && matchFilter) ? "" : "none";
        });
    }

});
