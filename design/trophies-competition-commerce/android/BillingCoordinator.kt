package com.lastlightcourier.billing

import android.app.Activity
import com.android.billingclient.api.BillingClient
import com.android.billingclient.api.BillingClientStateListener
import com.android.billingclient.api.BillingFlowParams
import com.android.billingclient.api.BillingResult
import com.android.billingclient.api.PendingPurchasesParams
import com.android.billingclient.api.ProductDetails
import com.android.billingclient.api.Purchase
import com.android.billingclient.api.PurchasesUpdatedListener
import com.android.billingclient.api.QueryProductDetailsParams
import com.android.billingclient.api.QueryPurchasesParams

/** Drop into an Android host after adding Play Billing Library and a secure verifier.
 *  Never grant gems or outfits from this client callback alone.
 */
class BillingCoordinator(
    private val activity: Activity,
    private val verifier: PurchaseVerifier,
    private val onCatalog: (List<ShopProduct>) -> Unit,
    private val onMessage: (String) -> Unit
) : PurchasesUpdatedListener {
    private val productIds = setOf("gems_small", "gems_medium", "outfit_marigold")
    private val details = mutableMapOf<String, ProductDetails>()
    private val billing = BillingClient.newBuilder(activity)
        .setListener(this)
        .enablePendingPurchases(PendingPurchasesParams.newBuilder().enableOneTimeProducts().build())
        .build()

    fun start() {
        billing.startConnection(object : BillingClientStateListener {
            override fun onBillingSetupFinished(result: BillingResult) {
                if (result.responseCode == BillingClient.BillingResponseCode.OK) {
                    refreshCatalog()
                    restore()
                } else onMessage("Google Play shop unavailable: ${result.debugMessage}")
            }
            override fun onBillingServiceDisconnected() { onMessage("Google Play shop disconnected; retry when available") }
        })
    }

    fun refreshCatalog() {
        if (!billing.isReady) return
        val requested = productIds.map { QueryProductDetailsParams.Product.newBuilder()
            .setProductId(it).setProductType(BillingClient.ProductType.INAPP).build() }
        billing.queryProductDetailsAsync(QueryProductDetailsParams.newBuilder().setProductList(requested).build()) { result, response ->
            if (result.responseCode != BillingClient.BillingResponseCode.OK) return@queryProductDetailsAsync onMessage(result.debugMessage)
            details.clear()
            response.productDetailsList.forEach { details[it.productId] = it }
            onCatalog(details.values.map { ShopProduct(it.productId, it.name, it.oneTimePurchaseOfferDetails?.formattedPrice ?: "") })
        }
    }

    fun buy(id: String) {
        if (id !in productIds || !billing.isReady) return onMessage("Product unavailable")
        val product = details[id] ?: return onMessage("Refresh the shop and try again")
        val offer = product.oneTimePurchaseOfferDetails ?: return onMessage("Product has no current offer")
        val params = BillingFlowParams.newBuilder().setProductDetailsParamsList(listOf(
            BillingFlowParams.ProductDetailsParams.newBuilder()
                .setProductDetails(product).setOfferToken(offer.offerToken).build()
        )).build()
        val result = billing.launchBillingFlow(activity, params)
        if (result.responseCode != BillingClient.BillingResponseCode.OK) onMessage(result.debugMessage)
    }

    fun restore() {
        if (!billing.isReady) return
        billing.queryPurchasesAsync(QueryPurchasesParams.newBuilder().setProductType(BillingClient.ProductType.INAPP).build()) { result, purchases ->
            if (result.responseCode == BillingClient.BillingResponseCode.OK) purchases.forEach(::process)
            else onMessage("Could not restore purchases: ${result.debugMessage}")
        }
    }

    override fun onPurchasesUpdated(result: BillingResult, purchases: MutableList<Purchase>?) {
        when (result.responseCode) {
            BillingClient.BillingResponseCode.OK -> purchases.orEmpty().forEach(::process)
            BillingClient.BillingResponseCode.USER_CANCELED -> onMessage("Purchase canceled")
            else -> onMessage("Purchase unavailable: ${result.debugMessage}")
        }
    }

    private fun process(purchase: Purchase) {
        if (purchase.products.any { it !in productIds }) return onMessage("Unknown purchase product")
        if (purchase.purchaseState == Purchase.PurchaseState.PENDING) return onMessage("Purchase pending; no items granted yet")
        if (purchase.purchaseState != Purchase.PurchaseState.PURCHASED) return
        // The verifier checks token, package, product, state, account and prior grant.
        // Its server consumes gem packs or acknowledges outfits only after an idempotent grant.
        verifier.submit(purchase.purchaseToken, purchase.products) { accepted ->
            activity.runOnUiThread { if (accepted) onMessage("Purchase verified; refresh entitlements") else onMessage("Purchase is awaiting verification") }
        }
    }

    fun close() = billing.endConnection()
}

data class ShopProduct(val id: String, val name: String, val formattedPrice: String)

interface PurchaseVerifier {
    fun submit(token: String, productIds: List<String>, complete: (Boolean) -> Unit)
}
