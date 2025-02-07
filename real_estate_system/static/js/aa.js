let sortDirection = true; // True for ascending, false for descending

function sortTable(columnIndex) {
    const table = document.getElementById("ejarTable");
    const rows = Array.from(table.rows).slice(1); // تجاهل رأس الجدول

    // تحديد نوع البيانات بناءً على العمود
    const firstRowValue = rows[0].cells[columnIndex].innerText.trim();

    const isNumeric = !isNaN(firstRowValue) && firstRowValue !== '';
    const isDate = !isNaN(Date.parse(firstRowValue));  // تحديد إذا كان التاريخ

    rows.sort((rowA, rowB) => {
        const cellA = rowA.cells[columnIndex].innerText.trim();
        const cellB = rowB.cells[columnIndex].innerText.trim();

        if (isDate) {
            // فرز التواريخ
            const dateA = new Date(cellA);
            const dateB = new Date(cellB);
            return sortDirection ? dateA - dateB : dateB - dateA;
        }

        if (isNumeric) {
            // فرز الأرقام
            return sortDirection ? parseFloat(cellA) - parseFloat(cellB) : parseFloat(cellB) - parseFloat(cellA);
        }

        // فرز النصوص
        return sortDirection ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
    });

    // إعادة إضافة الصفوف بعد الترتيب
    rows.forEach(row => table.appendChild(row));

    // تبديل الاتجاه (تصاعدي / تنازلي)
    sortDirection = !sortDirection;
}
