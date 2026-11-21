const categoryNames = {
  cars: "السيارات", houses: "المنازل", buildings: "المباني",
  memberships: "العضويات", other: "أخرى"
};
const grid = document.getElementById("products-grid");
const empty = document.getElementById("empty-products");
let selectedCategory = "all";

function renderProducts() {
  const list = (Array.isArray(products) ? products : []).filter(p =>
    selectedCategory === "all" || p.category === selectedCategory
  );
  grid.innerHTML = "";
  empty.hidden = list.length !== 0;
  list.forEach(product => {
    const card = document.createElement("article");
    card.className = "tile product-card";
    const img = document.createElement("img");
    img.className = "product-image";
    img.src = product.image;
    img.alt = product.name || "صورة المنتج";
    img.loading = "lazy";
    img.onerror = () => { img.style.display = "none"; };
    const category = document.createElement("span");
    category.className = "tag";
    category.textContent = categoryNames[product.category] || "منتج";
    const name = document.createElement("h3");
    name.textContent = product.name || "منتج جديد";
    const desc = document.createElement("p");
    desc.textContent = product.description || "";
    const price = document.createElement("div");
    price.className = "product-price";
    price.textContent = product.price || "السعر عند الطلب";
    const order = document.createElement("a");
    order.className = "btn product-order";
    order.href = "https://discord.gg/teXu4rFgZt";
    order.target = "_blank";
    order.rel = "noopener";
    order.textContent = "اطلب الآن";
    card.append(img, category, name, desc, price, order);
    grid.append(card);
  });
}
document.querySelectorAll(".filter").forEach(button => {
  button.addEventListener("click", () => {
    selectedCategory = button.dataset.category;
    document.querySelectorAll(".filter").forEach(b => b.classList.toggle("active", b === button));
    renderProducts();
  });
});
const paymentGrid = document.getElementById("payment-grid");
(paymentMethods || []).forEach(method => {
  const card = document.createElement("article");
  card.className = "tile payment-card";
  const title = document.createElement("h3");
  title.textContent = method.name;
  const details = document.createElement("p");
  details.textContent = method.details;
  card.append(title, details);
  paymentGrid.append(card);
});
renderProducts();
