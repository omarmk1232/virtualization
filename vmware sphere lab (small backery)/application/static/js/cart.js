const CART_KEY = 'moktech_bakery_cart';

function getCart() {
    return JSON.parse(localStorage.getItem(CART_KEY) || '[]');
}

function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    updateCartCount();
}

function updateCartCount() {
    const count = getCart().reduce((sum, item) => sum + item.quantity, 0);
    const el = document.getElementById('cart-count');
    if (el) el.textContent = count;
}

function addToCart(id, name, price) {
    const cart = getCart();
    const existing = cart.find(item => item.id === id);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ id, name, price, quantity: 1 });
    }
    saveCart(cart);
    flashCartBar();
    showAddedFeedback(id);
}

function removeFromCart(id) {
    saveCart(getCart().filter(item => item.id !== id));
    renderOrderCart();
}

function updateQuantity(id, delta) {
    const cart = getCart();
    const item = cart.find(i => i.id === id);
    if (!item) return;
    item.quantity += delta;
    if (item.quantity <= 0) {
        removeFromCart(id);
        return;
    }
    saveCart(cart);
    renderOrderCart();
}

function clearCart() {
    localStorage.removeItem(CART_KEY);
    updateCartCount();
}

function renderOrderCart() {
    const container = document.getElementById('cart-items-display');
    const totalEl = document.getElementById('cart-total-display');
    if (!container) return;

    const cart = getCart();
    if (cart.length === 0) {
        container.innerHTML = '<p class="empty-message">Your cart is empty. <a href="/menu">Browse our menu</a>.</p>';
        if (totalEl) totalEl.textContent = '0.00';
        updateCartCount();
        return;
    }

    let total = 0;
    container.innerHTML = cart.map(item => {
        const subtotal = item.price * item.quantity;
        total += subtotal;
        return `
        <div class="cart-item">
            <div class="cart-item-info">
                <span class="cart-item-name">${escHtml(item.name)}</span>
                <span class="cart-item-price">$${item.price.toFixed(2)} each</span>
            </div>
            <div class="cart-item-controls">
                <button class="qty-btn" onclick="updateQuantity(${item.id}, -1)">&#8722;</button>
                <span class="qty">${item.quantity}</span>
                <button class="qty-btn" onclick="updateQuantity(${item.id}, 1)">&#43;</button>
                <button class="remove-btn" onclick="removeFromCart(${item.id})">Remove</button>
            </div>
            <span class="cart-item-subtotal">$${subtotal.toFixed(2)}</span>
        </div>`;
    }).join('');

    if (totalEl) totalEl.textContent = total.toFixed(2);
    updateCartCount();
}

function flashCartBar() {
    const bar = document.getElementById('cart-bar');
    if (!bar) return;
    bar.classList.add('visible');
    const cart = getCart();
    const count = cart.reduce((s, i) => s + i.quantity, 0);
    const summary = document.getElementById('cart-summary');
    if (summary) summary.textContent = count + ' item' + (count !== 1 ? 's' : '') + ' in cart';
}

function showAddedFeedback(productId) {
    const btn = document.querySelector(`button[onclick*="addToCart(${productId},"]`);
    if (!btn) return;
    const orig = btn.textContent;
    btn.textContent = 'Added!';
    btn.classList.add('added');
    setTimeout(() => {
        btn.textContent = orig;
        btn.classList.remove('added');
    }, 1000);
}

function escHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

document.addEventListener('DOMContentLoaded', updateCartCount);
