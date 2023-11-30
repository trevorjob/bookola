var createCheckoutSession = function(priceId) {
    return fetch("/create-checkout-session", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            priceId: priceId
        })
    }).then(function(result) {
        return result.json();
    });
}

const PREMIUM_PRICE_MONTHLY_ID = "price_1OHpulLr3itnznEm553iHv2g";
const PLATINUM_PRICE_MONTHLY_ID = "price_1OHpydLr3itnznEm1hxM1If1";
const stripe = Stripe("pk_test_51OHcDoLr3itnznEm1btTbj4lDDqwvgVMWYjnTMQXpqRuc5eatNhu1zQbtVImmezCMeO37jaFMUYmdHUrefnFSr6c00TTGoIeVW");

document.addEventListener("DOMContentLoaded", function(event) {
    document
    .getElementById('checkout-premuim')
    .addEventListener("click", function(evt) {
        createCheckoutSession(PREMIUM_PRICE_MONTHLY_ID).then(function(data) {
            stripe
            .redirectToCheckout({
                sessionId: data.sessionId
            })
        })
    });
    document
    .getElementById("checkout-platinum")
    .addEventListener("click", function(evt) {
        createCheckoutSession(PLATINUM_PRICE_MONTHLY_ID).then(function(data) {
            stripe
            .redirectToCheckout({
                sessionId: data.sessionId
            });
        })
    });
})