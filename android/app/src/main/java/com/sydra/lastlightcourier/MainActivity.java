package com.sydra.lastlightcourier;

import android.app.Activity;
import android.os.Bundle;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.content.Context;
import android.graphics.Color;
import android.util.Log;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import java.io.InputStream;
import java.net.URLConnection;
import java.util.Locale;

public final class MainActivity extends Activity {
    private static final String ORIGIN = "https://appassets.androidplatform.net";
    private static final String START = ORIGIN + "/assets/www/index.html";
    private WebView web;
    private Vibrator vibrator;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(Color.rgb(20, 24, 39));
        getWindow().setNavigationBarColor(Color.rgb(20, 24, 39));
        vibrator = (Vibrator)getSystemService(Context.VIBRATOR_SERVICE);
        web = new WebView(this);
        web.setBackgroundColor(Color.rgb(20, 24, 39));
        web.getSettings().setJavaScriptEnabled(true);
        web.getSettings().setDomStorageEnabled(true);
        web.getSettings().setAllowFileAccess(false);
        web.getSettings().setAllowContentAccess(false);
        web.getSettings().setJavaScriptCanOpenWindowsAutomatically(false);
        web.getSettings().setMediaPlaybackRequiresUserGesture(false);
        web.addJavascriptInterface(new HapticBridge(), "CourierAndroid");
        web.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return !request.getUrl().toString().startsWith(ORIGIN + "/assets/www/");
            }
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();
                if (!url.startsWith(ORIGIN + "/assets/www/")) return new WebResourceResponse("text/plain", "UTF-8", null);
                String path = url.substring((ORIGIN + "/assets/").length()).split("\\?", 2)[0];
                if (path.contains("..")) return new WebResourceResponse("text/plain", "UTF-8", null);
                try {
                    InputStream stream = getAssets().open(path);
                    String mime = URLConnection.guessContentTypeFromName(path);
                    if (mime == null) mime = "application/octet-stream";
                    WebResourceResponse response = new WebResourceResponse(mime, "UTF-8", stream);
                    response.setResponseHeaders(java.util.Collections.singletonMap("Content-Security-Policy", "default-src 'self' data: blob:; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'none'"));
                    return response;
                } catch (Exception e) {
                    Log.e("CourierHost", "Missing local asset: " + path, e);
                    return new WebResourceResponse("text/plain", "UTF-8", null);
                }
            }
            @Override public void onReceivedError(WebView view, WebResourceRequest request, android.webkit.WebResourceError error) {
                if (request.isForMainFrame()) Log.e("CourierHost", "Page load failed: " + error.getDescription());
            }
        });
        setContentView(web);
        web.loadUrl(START);
    }

    private final class HapticBridge {
        @JavascriptInterface public void haptic(String kind) {
            if (kind == null || vibrator == null || !vibrator.hasVibrator()) return;
            long[] timings;
            switch (kind) {
                case "step": timings = new long[]{0, 10}; break;
                case "shadowNear": timings = new long[]{0, 28, 32, 35}; break;
                case "house": timings = new long[]{0, 24, 24, 45}; break;
                case "repair": timings = new long[]{0, 35, 28, 65}; break;
                case "denied": timings = new long[]{0, 55, 35, 55}; break;
                case "complete": timings = new long[]{0, 30, 40, 30, 40, 75}; break;
                case "failure": timings = new long[]{0, 75, 45, 100}; break;
                case "crossing": timings = new long[]{0, 18, 25, 18}; break;
                default: return;
            }
            Log.d("CourierHaptic", kind);
            vibrator.vibrate(VibrationEffect.createWaveform(timings, -1));
        }
    }

    @Override public void onBackPressed() {
        web.evaluateJavascript("window.CourierApp&&window.CourierApp.back()", result -> {
            if (!"true".equals(result)) super.onBackPressed();
        });
    }
    @Override protected void onPause() { super.onPause(); if (web != null) web.onPause(); }
    @Override protected void onResume() { super.onResume(); if (web != null) web.onResume(); }
    @Override protected void onDestroy() { if (web != null) web.destroy(); super.onDestroy(); }
}
