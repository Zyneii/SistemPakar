

/* ================ OPEN ADD MODAL ================ */
function openAddModal() {
    document.getElementById("modalAdd").style.display = "flex";
}
function closeAddModal() {
    document.getElementById("modalAdd").style.display = "none";
}


/* ================ OPEN EDIT MODAL ================ */
function openEditModal(btn) {

    // Ambil data dari tombol
    const id = btn.dataset.id;
    const nama = btn.dataset.nama || "";
    const solusi = btn.dataset.solusi || "";
    const antecedents = btn.dataset.antecedents || "";
    const penyakit = btn.dataset.penyakit || "";

    // ID input modal (nama input beda tiap halaman)
    const idField     = document.getElementById("edit_id");
    const namaField   = document.getElementById("edit_nama");
    const solusiField = document.getElementById("edit_solusi");
    const antField    = document.getElementById("edit_antecedents");
    const penField    = document.getElementById("edit_consequent");

    if (idField) idField.value = id;
    if (namaField) namaField.value = nama;
    if (solusiField) solusiField.value = solusi;
    if (antField) antField.value = antecedents;
    if (penField) penField.value = penyakit;

    // Set ACTION FORM otomatis
    const form = document.getElementById("formEdit");
    if (form) form.action = btn.dataset.action;

    document.getElementById("modalEdit").style.display = "flex";
}

function closeEditModal() {
    document.getElementById("modalEdit").style.display = "none";
}


/* ================ OPEN DELETE MODAL ================ */
function openDeleteModal(btn) {
    const id = btn.dataset.id;

    document.getElementById("delete_id_show").innerText = id;
    document.getElementById("delete_id").value = id;

    const form = document.getElementById("deleteForm");
    form.action = btn.dataset.action;

    document.getElementById("modalDelete").style.display = "flex";
}

function closeDeleteModal() {
    document.getElementById("modalDelete").style.display = "none";
}


/* ================ CLOSE WHEN CLICK OUTSIDE ================ */
window.onclick = function (e) {
    const addModal = document.getElementById("modalAdd");
    const editModal = document.getElementById("modalEdit");
    const deleteModal = document.getElementById("modalDelete");

    if (e.target === addModal) addModal.style.display = "none";
    if (e.target === editModal) editModal.style.display = "none";
    if (e.target === deleteModal) deleteModal.style.display = "none";
};

function openAddRuleModal() {
    document.getElementById("modalAddRule").style.display = "flex";
}
function closeAddRuleModal() {
    document.getElementById("modalAddRule").style.display = "none";
}


/* =====================================================
   OPEN & CLOSE MODAL: EDIT RULE
===================================================== */
function openEditRuleModal(id_rule, antecedents, penyakit) {

    // Set ID
    document.getElementById("edit_id_rule").value = id_rule;

    // SET GEJALA (checkbox)
    const selected = antecedents.split(",");
    document.querySelectorAll(".edit-gejala").forEach(cb => {
        cb.checked = selected.includes(cb.value);
    });

    // SET Penyakit
    document.getElementById("edit_penyakit").value = penyakit;

    // Set action form → sesuai Flask
    const form = document.getElementById("formEditRule");
    form.action = "/rule/edit/" + id_rule;

    document.getElementById("modalEditRule").style.display = "flex";
}

function closeEditRuleModal() {
    document.getElementById("modalEditRule").style.display = "none";
}


/* =====================================================
   OPEN & CLOSE MODAL: DELETE RULE
===================================================== */
function openDeleteRuleModal(id_rule) {

    document.getElementById("delete_rule_show").innerText = id_rule;

    const form = document.getElementById("formDeleteRule");

    // Arahkan ke route Flask yang benar
    form.action = "/rule/hapus/" + id_rule;

    document.getElementById("modalDeleteRule").style.display = "flex";
}

function closeDeleteRuleModal() {
    document.getElementById("modalDeleteRule").style.display = "none";
}


/* =====================================================
   CLOSE MODAL WHEN CLICK OUTSIDE
===================================================== */
window.onclick = function (e) {

    const add = document.getElementById("modalAddRule");
    const edit = document.getElementById("modalEditRule");
    const del  = document.getElementById("modalDeleteRule");

    if (e.target === add) add.style.display = "none";
    if (e.target === edit) edit.style.display = "none";
    if (e.target === del) del.style.display = "none";
};
