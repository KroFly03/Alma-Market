import { defineStore } from "pinia";
import { computed, ref, toRefs, watch } from "vue";
import { useLocalStorage } from "@/composables/useLocalStorage.js";
import { api } from "@/api/api.js";
import { useAuthStore } from "@/stores/authStore.js";

export const useCartStore = defineStore("cart", () => {
    const noAuthCartItems = useLocalStorage("cart", []);
    const authCartItems = ref([]);
    const updatingGoodsItemId = ref(null);

    const { isLoggedIn } = toRefs(useAuthStore());

    const lastAddedItem = ref(null);
    let lastAddedItemVisibleTimer;

    const setLastAddedItem = (item) => {
        lastAddedItem.value = null;
        setTimeout(() => (lastAddedItem.value = item), 50);

        clearTimeout(lastAddedItemVisibleTimer);
        lastAddedItemVisibleTimer = setTimeout(() => clearLastAddedItem(), 2000);
    };

    const clearLastAddedItem = () => {
        lastAddedItem.value = null;
    };

    const fetchBasket = async () => {
        const items = await api.basket.get();

        authCartItems.value = items.map(({ amount, item }) => ({
            item: formatGoodsItemForCart(item),
            quantity: amount,
        }));
    };

    watch(
        () => isLoggedIn.value,
        async () => {
            if (isLoggedIn.value) await fetchBasket();
        }
    );

    const tryGetCartItem = (goodsItem) => {
        return cartItems.value.find((cartItem) => cartItem.item.id === goodsItem.id);
    };

    const addToCart = async (goodsItem) => {
        if (isLoggedIn.value) {
            await api.basket.add({ goodsItemId: goodsItem.id, amount: 1 });
        }

        const cartItem = tryGetCartItem(goodsItem);

        if (cartItem) cartItem.quantity++;
        else {
            const cartItem = formatGoodsItemForCart(goodsItem);

            setLastAddedItem(cartItem);
            cartItems.value.push({ quantity: 1, item: cartItem });
        }
    };

    const formatGoodsItemForCart = (goodsItem) => ({
        id: goodsItem.id,
        name: goodsItem.name,
        image: goodsItem.image,
        price: goodsItem.price,
        amount: goodsItem.amount,
    });

    const removeFromCart = async (goodsItem) => {
        if (isLoggedIn.value) await api.basket.remove({ goodsItemId: goodsItem.id });

        const cartItemIdx = cartItems.value.indexOf(tryGetCartItem(goodsItem));
        cartItems.value.splice(cartItemIdx, 1);
    };

    const fetchUpdateCartItemQuantity = async (goodsItemId, newQuantity) => {
        updatingGoodsItemId.value = goodsItemId;
        await api.basket.update({ goodsItemId, amount: newQuantity });
        updatingGoodsItemId.value = null;
    };

    const incrementQuantity = async (cartItem) => {
        if (cartItem.quantity + 1 < cartItem.item.amount) {
            const newQuantity = cartItem.quantity + 1;

            if (isLoggedIn.value) await fetchUpdateCartItemQuantity(cartItem.item.id, newQuantity);

            cartItem.quantity = newQuantity;
        }
    };

    const decrementQuantity = async (cartItem) => {
        if (cartItem.quantity > 1) {
            const newQuantity = cartItem.quantity - 1;

            if (isLoggedIn.value) await fetchUpdateCartItemQuantity(cartItem.item.id, newQuantity);

            cartItem.quantity = newQuantity;
        }
    };

    const cartItems = computed(() => {
        if (!isLoggedIn.value) return noAuthCartItems.value;

        return authCartItems.value;
    });

    const inCart = (goodsItem) => {
        return Boolean(tryGetCartItem(goodsItem));
    };

    const cartTotalPrice = computed(() => {
        return cartItems.value.reduce(
            (accum, cartItem) => accum + cartItem.quantity * cartItem.item.price,
            0
        );
    });

    const clearCart = () => {
        cartItems.value.splice(0, cartItems.value.length);
    };

    return {
        cartItems,
        lastAddedItem,
        clearLastAddedItem,
        addToCart,
        removeFromCart,
        incrementQuantity,
        decrementQuantity,
        updatingGoodsItemId,
        inCart,
        cartTotalPrice,
        clearCart,
    };
});
