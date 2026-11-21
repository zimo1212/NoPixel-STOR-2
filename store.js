
// ========================================
// أسماء التصنيفات التي تظهر للزوار
// ========================================
const categoryNames = {
    cars: "السيارات",
    houses: "المنازل",
    buildings: "المباني",
    memberships: "العضويات",
    other: "أخرى"
};

// عناصر صفحة المنتجات
const grid = document.getElementById("products-grid");
const empty = document.getElementById("empty-products");

// التصنيف المحدد افتراضياً
let selectedCategory = "all";

// ========================================
// عرض المنتجات
// ========================================
function renderProducts() {

    // فلترة المنتجات حسب التصنيف المحدد
    const list = (Array.isArray(products) ? products : []).filter(product =>
        selectedCategory === "all" ||
        product.category === selectedCategory
    );

    // تفريغ القائمة قبل إعادة عرض المنتجات
    grid.innerHTML = "";

    // إظهار رسالة عدم وجود منتجات عند الحاجة
    empty.hidden = list.length !== 0;

    // إنشاء بطاقة لكل منتج
    list.forEach(product => {

        const card = document.createElement("article");
        card.className = "tile product-card";

        // صورة المنتج
        const img = document.createElement("img");
        img.className = "product-image";
        img.src = product.image;
        img.alt = product.name || "صورة المنتج";
        img.loading = "lazy";

        // إخفاء الصورة إذا لم يتم العثور عليها
        img.onerror = () => {
            img.style.display = "none";
        };

        // تصنيف المنتج
        const category = document.createElement("span");
        category.className = "tag";
        category.textContent =
            categoryNames[product.category] || "منتج";

        // اسم المنتج
        const name = document.createElement("h3");
        name.textContent = product.name || "منتج جديد";

        // وصف المنتج
        const desc = document.createElement("p");
        desc.textContent = product.description || "";

        // سعر المنتج
        const price = document.createElement("div");
        price.className = "product-price";
        price.textContent = product.price || "السعر عند الطلب";

        // زر طلب المنتج عبر الديسكورد
        const order = document.createElement("a");
        order.className = "btn product-order";
        order.href = "https://discord.gg/teXu4rFgZt";
        order.target = "_blank";
        order.rel = "noopener noreferrer";
        order.textContent = "اطلب الآن";

        // إضافة العناصر إلى بطاقة المنتج
        card.append(
            img,
            category,
            name,
            desc,
            price,
            order
        );

        // إضافة البطاقة إلى شبكة المنتجات
        grid.append(card);
    });
}

// ========================================
// أزرار تصفية المنتجات حسب التصنيف
// ========================================
document.querySelectorAll(".filter").forEach(button => {

    button.addEventListener("click", () => {

        // تحديد التصنيف المختار
        selectedCategory = button.dataset.category;

        // تحديث شكل الزر النشط
        document.querySelectorAll(".filter").forEach(b => {
            b.classList.toggle("active", b === button);
        });

        // إعادة عرض المنتجات
        renderProducts();
    });
});

// ========================================
// عرض طرق الدفع
// ========================================
const paymentGrid = document.getElementById("payment-grid");

(paymentMethods || []).forEach(method => {

    const card = document.createElement("article");
    card.className = "tile payment-card";

    // اسم طريقة الدفع
    const title = document.createElement("h3");
    title.textContent = method.name;

    // تفاصيل طريقة الدفع
    const details = document.createElement("p");
    details.textContent = method.details;

    // إضافة البيانات إلى البطاقة
    card.append(title, details);

    // إضافة البطاقة إلى شبكة الدفع
    paymentGrid.append(card);
});

// ========================================
// تشغيل عرض المنتجات عند تحميل الملف
// ========================================
renderProducts();
